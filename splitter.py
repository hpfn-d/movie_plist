#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
from zetcode tutorial
"""

# import sys
# import time
import urllib.request
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QSplitter, QListWidget)
from PyQt5.QtCore import *
from PyQt5.QtGui import *


# class MyListWidget(QListWidget):
#
#    def Clicked(self, item):
#        print(self.currentItem().text())
#        QMessageBox.information(self, "ListWidget", "You clicked: " + item.text())


class TwoLines(QWidget):
    def __init__(self):
        super().__init__()

        self.bottom = QLabel()
        self.top = QListWidget()
        self.init_ui()

    def init_ui(self):
        hbox = QHBoxLayout(self)

        self.top.addItem("item 1")
        self.top.addItem("item 2")
        self.top.addItem("item 3")
        self.top.addItem("item 4")
        self.top.setCurrentRow(0)
        # self.top.itemClicked.connect(self.top.Clicked)

        # bottom = QFrame(self)
        # bottom.setFrameShape(QFrame.StyledPanel)
        self.bottom.setText(self.top.currentItem().text())

        def changed_item():
            if self.top.currentItem():
                img = QImage()  # (8,10,4)
                data = urllib.request.urlopen(
                    "https://images-na.ssl-images-amazon.com/images/M/MV5BMTc5Mzg3NjI4OF5BMl5BanBnXkFtZTgwNzA3Mzg4MDI@._V1_UX182_CR0,0,182,268_AL_.jpg").read()
                img.loadFromData(data)
                img.save('picture.png')
                texto = '<html><table><td><img src="picture.png"></td><td>' + self.top.currentItem().text() + '</td></table></html>'
                # self.bottom.setText(self.top.currentItem().text())
                # self.bottom.setOpenExternalLinks(True)
                self.bottom.setText(texto)
                # self.bottom.setPixmap(QPixmap(img))

        self.top.currentItemChanged.connect(changed_item)

        splitter1 = QSplitter(Qt.Vertical)
        splitter1.addWidget(self.top)
        splitter1.addWidget(self.bottom)

        hbox.addWidget(splitter1)
        self.setLayout(hbox)

    #        self.setGeometry(300, 300, 300, 200)
    #        self.setWindowTitle('QSplitter')
    #        self.show()

    def on_changed(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()

# if __name__ == '__main__':
#
#    app = QApplication(sys.argv)
#    ex = TwoLines()
#    sys.exit(app.exec_())
