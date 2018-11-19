#coding: utf-8

import configparser
import os
import pickle

from PyQt5.QtWidgets import (QCompleter, QComboBox, QTableView)
from PyQt5.QtCore import *

# Config here
class config():

    con = None

    config_dir = ".config"

    def __init__(self):

        self.con = configparser.ConfigParser()

        if (os.path.exists(self.config_dir)):

            self.con.read(self.config_dir)

        else:

            self.con['SERVER'] = {'email': '', 'smtp': '', 'port': '', 'username':'', 'password':''}
            with open(self.config_dir, 'w') as configfile:
                self.con.write(configfile)


    def get_email(self):
        try:
            return self.con["SERVER"]["email"]
        except KeyError as e:
            return None
        except:
            raise

    def get_smtp(self):
        try:
            return self.con["SERVER"]["smtp"]
        except KeyError as e:
            return None
        except:
            raise

    def get_port(self):
        try:
            return int(self.con["SERVER"]["port"])
        except KeyError as e:
            return None
        except:
            raise

    def get_username(self):
        try:
            return self.con["SERVER"]["username"]
        except KeyError as e:
            return None
        except:
            raise

    def get_password(self):
        try:
            return self.con["SERVER"]["password"]
        except KeyError as e:
            return None
        except:
            raise

def load_pkl(filename):
    with open(filename + '.pkl', 'rb') as f:
        return pickle.load(f)


class EmojiTableModel(QAbstractTableModel):

    emojiL = None

    def __init__(self, emojiL, parent=None):

        super().__init__(parent=parent)

        self.emojiL = emojiL

    def rowCount(self, parent):
        return len(self.emojiL)

    def columnCount(self, parent):
        return len(self.emojiL[0])

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return "{0}".format(self.emojiL[index.row()][index.column()])



class EmojiTable(QComboBox):

    view = None
    model = None

    emojiChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        emoji2 = load_pkl("emoji2")

        emoji = []

        num_cols = 5
        for category in ["People", "Nature", "Food", "Activity", "Travel", "Objects", "Symbols", "Flags"]:
            col = 0
            for i in emoji2[category]:
                if col % num_cols == 0:
                    col = 0
                    emoji.append([])

                emoji[-1].append(i["value"])
                col += 1
            while not col % num_cols == 0:
                emoji[-1].append("")
                col += 1


        self.model = EmojiTableModel(emoji, parent=self)
        self.view = QTableView()

        self.view.setMinimumSize(300, 200)



        self.view.setShowGrid(False)

        self.view.verticalHeader().setVisible(False)
        self.view.horizontalHeader().setVisible(False)

        self.view.horizontalHeader().setSectionResizeMode(1)
        self.view.verticalHeader().setSectionResizeMode(1)
        #self.view.setMaximumWidth(200)
        self.view.setStyleSheet("font-size: 23px;")

        self.setStyleSheet('''* {font-size: 23px; border: 0px; padding: 0px; background-color: rgba(255,255,255,0);} 
                                *::down-arrow {image: url(noimg); border-width: 0px;}
                                *::drop-down {border: none; width: 0px;}
                                }''')

        self.setModel(self.model)
        self.setView(self.view)

        self.activated.connect(self.set_col)

    def set_col(self, index):
        index2 = self.view.currentIndex()
        if not index2.isValid():
            return
        self.setModelColumn(index2.column())

        self.emojiChanged.emit(self.currentText())



