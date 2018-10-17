#coding: utf-8

import maildown as mail
from PyQt5.QtCore import *
from PyQt5.QtWidgets import (QApplication,
        QWidget,
        QFileDialog,
        QListWidgetItem,
        QShortcut
        )

from PyQt5.QtGui import QKeySequence
import os
import helper


app = QApplication([])
from ui_mwindow import Ui_MWindow
from ui_recipientswindow import Ui_recipientsWindow


# Set data for mailing-list and placeholders
class recipientsWindow(QWidget, Ui_recipientsWindow):
    ready = pyqtSignal()


    row_cnt = 2

    def __init__(self, parent=None):
        super().__init__(parent)

        self.table.setRowCount(self.row_cnt)
        self.table.setColumnCount(1)

        self.table.setHorizontalHeaderLabels(["EMail"])

        self.placeholders.textChanged.connect(self.set_labels)
        self.table.cellChanged.connect(self.adapt_size)

        self.save_close.pressed.connect(self.save_close_)
    def set_labels(self, text):

        labels = text.split(", ")
        self.table.setColumnCount(len(labels) + 1)
        self.table.setHorizontalHeaderLabels(["EMail"] + labels)

    def save_close_(self):
        self.ready.emit()


    def get_recipients(self):

        email_dict = {}
        email = ""


        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)

                if col == 0:
                    if item == None:
                        break
                    else:
                        i_text = item.text()
                        email = i_text
                        email_dict[i_text] = {}
                        continue

                if item == None:
                    continue

                email_dict[email][self.table.horizontalHeaderItem(col).text()] = item.text()


        return email_dict

    def adapt_size(self, r, c):
        if (c == 0 and r > self.row_cnt - 3):
            self.row_cnt = r + 3
            self.table.setRowCount(self.row_cnt)


class MDMailer_(QObject, mail.MDMailer):

    finished_sending = pyqtSignal()
    progress1 = pyqtSignal(int)
    progress2 = pyqtSignal(int)

    mail_text = None
    subject = None
    rec = None
    files = []

    def __init__(self, mymail, smtpserver, port, username, password):
        super().__init__(mymail=mymail,
                        smtpserver=smtpserver,
                        port=port,
                        username=username,
                        password=password)

    @pyqtSlot()
    def send(self):
        print("sending")
        self.send_mail(self.mail_text, self.subject, self.rec, files=self.files)
        print("finished")

    def progress(self, done, recipients_number):
        self.progress2.emit(recipients_number)
        self.progress1.emit(done)


class MWindow(QWidget, Ui_MWindow):


    # MDMailer Class handles everything except graphics
    mdm = None

    # recipientsWindow
    recWin = recipientsWindow()

    Mail_Thread = QThread()
    config = helper.config()

    send_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)


        # construct MDMailer with server Info
        self.mdm = MDMailer_(self.config.get_email(),
                             self.config.get_smtp(),
                             self.config.get_port(),
                             self.config.get_username(),
                             self.config.get_password())


        # Connect Stuff here ...
        self.mdtext.textChanged.connect(self.compile)
        self.send_btn.pressed.connect(self.send)
        self.add_att_btn.pressed.connect(self.add_att)
        self.send_signal.connect(self.mdm.send)
        self.mdm.finished_sending.connect(self.reenable_send)
        self.mdm.progress2.connect(self.progress_bar.setMaximum)
        self.mdm.progress1.connect(self.progress_bar.setValue)
        self.multi_rec_btn.pressed.connect(self.open_recipientsWindow)
        self.recWin.ready.connect(self.get_recipients)

        del_att_short = QShortcut(QKeySequence(Qt.Key_Delete), self.attachments)
        del_att_short.activated.connect(self.del_att)

        self.stylesheet = """
        .QPushButton {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 5px 11px;
            text-align: center;
            text-decoration: none;
            font-size: 16px;
            }
        .QPushButton:hover {
            background-color: #555;
            border: none;
            color: white;
            padding: 5px 11px;
            text-align: center;
            text-decoration: none;
            font-size: 16px;
            }
        .QLineEdit {
            background-color: #ddd;
            font-size: 16px;
            border-radius: 0px;
            }
        .QPlainTextEdit {
            background-color: #fff;
            font-size: 16px;
            border-radius: 0px;
            }
        .QFileDialog:QPushButton {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 5px 11px;
            text-align: center;
            text-decoration: none;
            font-size: 16px;
            }
        .QListWidget {
            background-color: #fff;
            font-size: 16px;
            }
        .QProgressBar {
            color: #FFFFFF;
            border: none;
            padding: 0px 0px;
            margin: -3px;
            border-radius: 0px;
            }
        .QProgressBar:chunk {
            background-color: #4CAF50;
            border: none;
            padding: 0px 0px;
            margin: 0px;
            border-radius: 0px;
            }
        """

        self.setStyleSheet(self.stylesheet)

        self.Mail_Thread.start()
        self.mdm.moveToThread(self.Mail_Thread)

    # Show html from plain text
    def compile(self):

        html_c = self.mdm.get_html(self.mdtext.toPlainText(), self.subject_edit.text())

        self.html_view.setHtml(html_c)

    # Send Mail
    def send(self):
        self.mdm.mail_text = self.mdtext.toPlainText()
        self.mdm.subject = self.subject_edit.text()
        to = self.to_edit.text()

        if to != "":
            rec = [to]
            self.mdm.rec = rec

        files = []
        for i in range(self.attachments.count()):
            files.append(str(self.attachments.item(i).data(3)))


        self.mdm.files = files

        #self.mdm.send_mail(mail_text, subject, rec, files=files)
        self.send_signal.emit()
        self.send_signal.disconnect()

    def add_att(self):
        fd = QFileDialog()
        files = fd.getOpenFileNames()

        for f in files[0]:
            item = QListWidgetItem()
            item.setData(3, f)
            item.setText(os.path.basename(f))
            self.attachments.addItem(item)

    def del_att(self):

        for item in self.attachments.selectedItems():
            tmp = self.attachments.takeItem(self.attachments.row(item))
            del tmp

    def open_recipientsWindow(self):
        self.recWin.show()

    def get_recipients(self):
        self.mdm.rec = self.recWin.get_recipients()
        self.recWin.close()

    @pyqtSlot()
    def reenable_send(self):
        self.send_signal.connect(self.mdm.send)

# here we go ...
window = MWindow()
window.show()

app.exec_()
