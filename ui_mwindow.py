#coding: utf-8

from PyQt5.QtWidgets import (
        QPushButton,
        QHBoxLayout,
        QVBoxLayout,
        QLineEdit,
        QPlainTextEdit,
        QListWidget,
        QProgressBar
        )

from PyQt5.Qt import QAbstractItemView, QWebView

from MdTextEdit import QPlainMdTextEdit

class Ui_MWindow():
    # Two column Layout
    layout_top = QHBoxLayout()

    # Vertical layout for each column
    layout_l = QVBoxLayout()
    layout_r = QVBoxLayout()

    # Horizontal layout for controls
    layout_r_h = QHBoxLayout()

    # Edit raw markdown
    mdtext = QPlainMdTextEdit()

    # shows html
    html_view = QWebView()

    # Mail Subject
    subject_edit = QLineEdit()

    # Recipient Mail
    to_edit = QLineEdit()

    # Open recipientsWindow
    multi_rec_btn = QPushButton()

    # Send EMail
    send_btn = QPushButton()

    # Add attachment
    add_att_btn = QPushButton()

    # QProgressBar
    progress_bar = QProgressBar()

    # attachment QListWidget
    attachments = QListWidget()


    def __init__(self):
        # build layout
        self.layout_l.addWidget(self.subject_edit)
        self.subject_edit.setPlaceholderText("Subject")
        self.layout_l.addWidget(self.mdtext)

        self.layout_r.addLayout(self.layout_r_h)
        self.layout_r_h.addWidget(self.to_edit)
        self.to_edit.setPlaceholderText("To:")

        self.layout_r_h.addWidget(self.multi_rec_btn)
        self.multi_rec_btn.setText("...")

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

        # other
        self.attachments.setSelectionMode(QAbstractItemView.ExtendedSelection)

