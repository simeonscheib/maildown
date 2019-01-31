from PyQt5.QtWidgets import (QWidget, QPlainTextEdit, QHBoxLayout, QPushButton, QFileDialog, QToolButton, QMainWindow, QToolBar, QAction)
import helper
from PyQt5.QtCore import pyqtSignal

class QPlainMdTextEdit(QMainWindow):

    textedit = None

    completer = None
    toolBar = None

    emtab = None
    texttab = None

    md_menu = None

    save_md_act = None
    load_md_act = None

    def __init__(self, parent=None):
        super().__init__(parent)

        self.textedit = QPlainTextEdit()

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.textedit)

        self.setCentralWidget(self.textedit)

        self.emtab = helper.EmojiTable()

        self.emtab.emojiChanged.connect(self.insert)
        self.emtab.setMinimumWidth(40)
        self.texttab = helper.TextTable()
        self.texttab.setMinimumWidth(70)

        self.texttab.insert.connect(self.insert)

        self.toolBar = QToolBar()

        self.addToolBar(self.toolBar)

        self.toolBar.addWidget(self.emtab)
        self.toolBar.addWidget(self.texttab)

        self.md_menu = QToolButton()
        self.md_menu.setText("md")
        self.md_menu.setStyleSheet('''
        * {
            font-size: 24px;
        }
        ''')
        self.md_menu.setPopupMode(2)

        self.save_md_act = QAction("save")
        self.load_md_act = QAction("load")

        self.md_menu.addAction(self.save_md_act)
        self.md_menu.addAction(self.load_md_act)

        self.toolBar.addWidget(self.md_menu)

        self.load_md_act.triggered.connect(self.load_md)

        self.save_md_act.triggered.connect(self.save_md)


        self.textedit.setStyleSheet('''
            * {
                padding-top: 25px;
                padding-left: 25px;
            }
        
        ''')



    def insert(self, text):
        self.textedit.insertPlainText(text)
        self.setFocus()

    def save_md(self):
        filename, t = QFileDialog.getSaveFileName(None, "Save to Markdown", ".md", "Markdown (*.md)")

        if filename == "":
            return

        if t == "Markdown (*.md)":
            with open(filename, "w") as file:
                file.write(self.textedit.toPlainText())


    def load_md(self):
        filename, t = QFileDialog.getOpenFileName(None, "Load Markdown", ".md", "Markdown (*.md)")

        if filename == "":
            return

        with open(filename, "r") as file:
            self.textedit.setPlainText(file.read())
