from PyQt5.QtWidgets import (QPlainTextEdit)
import helper

class QPlainMdTextEdit(QPlainTextEdit):

    completer = None
    emtab = None

    def __init__(self, parent=None):
        super().__init__(parent)

        self.emtab = helper.EmojiTable(self)

        self.emtab.emojiChanged.connect(self.insertEmoji)

        self.setStyleSheet('''
            * {padding-top: 25px;}
        
        ''')



    def insertEmoji(self, i):
        self.insertPlainText(i)
        self.setFocus()