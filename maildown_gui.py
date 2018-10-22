#coding: utf-8

import maildown as mail
from PyQt5.QtCore import *
from PyQt5.QtWidgets import (QApplication,
        QWidget,
        QFileDialog,
        QListWidgetItem,
        QShortcut,
        QMessageBox,
        QTableWidgetItem
        )

from PyQt5.QtGui import QKeySequence
import os
import helper
import csv


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

        for row in range(self.table.rowCount()):
            self.table.setItem(row, 0, QTableWidgetItem())
            self.table.item(row, 0).setCheckState(Qt.Checked)

        self.table.setHorizontalHeaderLabels(["EMail"])

        self.placeholders.textChanged.connect(self.set_labels)
        self.table.currentCellChanged.connect(self.adapt_size)

        self.save_close.pressed.connect(self.save_close_)
        self.save_csv.pressed.connect(self.save_csv_)
        self.load_csv.pressed.connect(self.load_csv_)

    def set_labels(self, text):

        labels = text.split(", ")
        self.table.setColumnCount(len(labels) + 1)
        self.table.setHorizontalHeaderLabels(["EMail"] + labels)

    def save_close_(self):
        self.ready.emit()


    def get_recipients(self):

        if self.one_mail.isChecked():
            return [self.get_recipients_str()]

        email_dict = {}
        email = ""


        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)

                if col == 0:
                    if item == None or item.text() == "" or item.checkState() == False:
                        break
                    else:
                        i_text = item.text()
                        email = i_text
                        email_dict[i_text] = {}
                        continue

                if item == None or item.text() == "":
                    continue

                email_dict[email][self.table.horizontalHeaderItem(col).text()] = item.text()


        return email_dict


    def get_recipients_str(self):

        rec_list = []

        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)

            if item == None or item.text() == "" or item.checkState() == False:
                continue
            else:
                rec_list.append(item.text())

        return ", ".join(rec_list)

    def adapt_size(self, r, c):
        if (c == 0 and r > self.row_cnt - 2):
            self.table.setRowCount(self.row_cnt + 1)
            self.table.setItem(r + 1, 0, QTableWidgetItem())
            self.table.item(r + 1, 0).setCheckState(Qt.Checked)
            self.row_cnt = r + 2


    def save_csv_(self):

        filename, t = QFileDialog.getSaveFileName(self, "Save to CSV", "maillist.csv", "CSV File (*.csv)")

        if filename == "":
            return

        if t == "CSV File (*.csv)":

            self.dump_to_csv(filename)

    def load_csv_(self):

        filename, t = QFileDialog.getOpenFileName(self, "Load CSV", filter="CSV File (*.csv)")

        if filename == "":
            return

        if t == "CSV File (*.csv)":

            empty = True

            for row in range(self.table.rowCount()):
                for col in range(self.table.columnCount()):

                    item = self.table.item(row, col)

                    if item != None and item.text() != "":
                        empty = False
                        break

                if not empty:
                    break

            if not empty:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Question)
                msg_box.setWindowTitle("Overwrite?")
                msg_box.setText("Table is not empty")
                msg_box.setInformativeText("Do you want to overwrite it?")
                msg_box.addButton(QMessageBox.Yes)
                msg_box.addButton(QMessageBox.Cancel)
                msg_box.setDefaultButton(QMessageBox.Cancel)

                answer = msg_box.exec()

                if answer == QMessageBox.Cancel:
                    return

            self.load_from_csv(filename)

    def dump_to_csv(self, filename):

        headers = []

        for col in range(self.table.columnCount()):
            headers.append(self.table.horizontalHeaderItem(col).text())


        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)

            writer.writerow(headers)

            for row in range(self.table.rowCount()):

                row_items = []

                for col in range(self.table.columnCount()):

                    item = self.table.item(row, col)

                    if item == None:
                        text = ""
                    else:
                        text = item.text()

                    row_items.append(text)

                if row_items.count("") == len(row_items):
                    continue

                writer.writerow(row_items)

    def load_from_csv(self, filename):

        with open(filename, newline='') as csvfile:

            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')

            firstline = next(reader)

            #self.table.setColumnCount(len(firstline))
            #self.table.setHorizontalHeaderLabels(firstline)

            self.placeholders.setText(", ".join(firstline[1:]))

            for i, row in enumerate(reader):
                for j, text in enumerate(row):
                    if j == 0:
                        self.adapt_size(i, j)
                        self.table.item(i, j).setText(text)
                    else:
                        self.table.setItem(i, j, QTableWidgetItem(text))


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
        try:
            self.send_mail(self.mail_text, self.subject, self.rec, files=self.files)
            print("finished")
        except Exception as e:
            print(str(e))
        self.finished_sending.emit()

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
        else:
            if self.mdm.rec == [""]:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setWindowTitle("No valid E-Mail address found")
                msg_box.setInformativeText("No valid E-Mail address found")

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
