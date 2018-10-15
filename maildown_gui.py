import maildown as mail
from PyQt5.QtCore import *
from PyQt5.QtWidgets import (QApplication,
        QWidget,
        QPushButton,
        QHBoxLayout,
        QVBoxLayout,
        QLineEdit,
        QPlainTextEdit,
        QListWidget,
        QFileDialog,
        QListWidgetItem,
        QShortcut,
        QTableWidget,
        QProgressBar
        )
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QKeySequence
from PyQt5.Qt import QAbstractItemView
import os
import helper


app = QApplication([])



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

class MWindow(QWidget):

    # Two column Layout
    layout_top = QHBoxLayout()

    # Vertical layout for each column
    layout_l = QVBoxLayout()
    layout_r = QVBoxLayout()

    # Horizontal layout for controls
    layout_r_h = QHBoxLayout()

    # Edit raw markdown
    mdtext = QPlainTextEdit()

    # shows html
    html_view = QWebEngineView()

    # Mail Subject
    subject_edit = QLineEdit()

    # Recipient Mail
    to_edit = QLineEdit()

    # Send EMail
    send_btn = QPushButton()

    # Add attachment
    add_att_btn = QPushButton()

    # QProgressBar
    progress_bar = QProgressBar()

    # attachment QListWidget
    attachments = QListWidget()

    # MDMailer Class handles everything except graphics
    mdm = None

    Mail_Thread = QThread()
    config = helper.config()

    send_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # build layout
        self.layout_l.addWidget(self.subject_edit)
        self.subject_edit.setPlaceholderText("Subject")
        self.layout_l.addWidget(self.mdtext)

        self.layout_r.addLayout(self.layout_r_h)
        self.layout_r_h.addWidget(self.to_edit)
        self.to_edit.setPlaceholderText("To:")

        self.layout_r_h.addWidget(self.send_btn)
        self.send_btn.setText("Send")

        self.layout_r_h.addWidget(self.add_att_btn)
        self.add_att_btn.setText("Attach..")

        self.attachments.setMaximumHeight(100)
        self.layout_r.addWidget(self.html_view)

        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(10)
        self.progress_bar.setValue(1)
        self.layout_r.addWidget(self.progress_bar)
        self.layout_r.addWidget(self.attachments)
        self.layout_top.addLayout(self.layout_l)
        self.layout_top.addLayout(self.layout_r)
        self.setLayout(self.layout_top)

        # construct MDMailer with server Info
        self.mdm = MDMailer_(self.config.get_email(),
                             self.config.get_smtp(),
                             self.config.get_port(),
                             self.config.get_username(),
                             self.config.get_password())

        # other

        self.attachments.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # Connect Stuff here ...
        self.mdtext.textChanged.connect(self.compile)
        self.send_btn.pressed.connect(self.send)
        self.add_att_btn.pressed.connect(self.add_att)
        self.send_signal.connect(self.mdm.send)
        self.mdm.finished_sending.connect(self.reenable_send)
        self.mdm.progress2.connect(self.progress_bar.setMaximum)
        self.mdm.progress1.connect(self.progress_bar.setValue)


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
        self.html_view.setHtml(
            self.mdm.get_html(self.mdtext.toPlainText(),
            self.subject_edit.text())
            )

    # Send Mail
    def send(self):
        self.mdm.mail_text = self.mdtext.toPlainText()
        self.mdm.subject = self.subject_edit.text()
        to = self.to_edit.text()
        #rec = {to, []}
        rec = {}
        for i in to.split(", "):
            rec[i] = {"Name" : i}

        files = []
        for i in range(self.attachments.count()):
            files.append(str(self.attachments.item(i).data(3)))

        self.mdm.rec = rec
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

    @pyqtSlot()
    def reenable_send(self):
        self.send_signal.connect(self.mdm.send)

# here we go ...
window = MWindow()
window.show()

app.exec_()
