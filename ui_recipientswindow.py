#coding: utf-8

from PyQt5.QtWidgets import (
        QPushButton,
        QHBoxLayout,
        QVBoxLayout,
        QLineEdit,
        QTableWidget,
        QCheckBox
        )

class Ui_recipientsWindow():
    layout_top = QVBoxLayout()

    layout_top_h = QHBoxLayout()

    one_mail = QCheckBox()

    load_csv = QPushButton()

    save_csv = QPushButton()

    save_close = QPushButton()

    placeholders = QLineEdit()

    table = QTableWidget()

    def __init__(self):
        self.placeholders.setPlaceholderText("Placeholder1, Placeholder2, ...")
        self.layout_top_h.addWidget(self.placeholders)

        self.one_mail.setText("Send one mail to all recipients")
        self.layout_top_h.addWidget(self.one_mail)

        self.load_csv.setText("Load CSV")
        self.layout_top_h.addWidget(self.load_csv)

        self.save_csv.setText("Save CSV")
        self.layout_top_h.addWidget(self.save_csv)

        self.save_close.setText("Save && Close")
        self.layout_top_h.addWidget(self.save_close)
        self.layout_top.addLayout(self.layout_top_h)
        self.layout_top.addWidget(self.table)

        self.setLayout(self.layout_top)

