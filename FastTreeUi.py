import os

from PySide6.QtCore import Qt, QEvent, QTimer
from PySide6.QtGui import QStandardItemModel, QStandardItem, QPixmap, QPainter, QColor, QFont
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QComboBox, QMainWindow, QApplication, QLabel, QMessageBox

import Fasttree
import finderRes
import iqTree
import model_finder
import mrbayes
import treeUI


class Stats(QMainWindow):
    def __init__(self,time,select):
        super().__init__()
        self.ui = QUiLoader().load('ui/FastTree.ui')
        self.setRotatedLabel('FastTree')
        self.ui.fasttree.clicked.connect(lambda:self.FastTree(time))
        self.ui.modelfinder_button.clicked.connect(lambda:self.modelFinder(time))
        self.ui.pic.clicked.connect(lambda:self.seeTreePic(time))
        self.ui.model_results.clicked.connect(lambda:self.seeFinderRes(time))

    def seeFinderRes(self,time):
        self.seeRes = finderRes.Stats(time)
        self.seeRes.ui.show()
    def setRotatedLabel(self, text):
        label = self.ui.findChild(QLabel, 'label_3')
        if label is not None:
            pixmap = QPixmap(label.width(), label.height())
            pixmap.fill(Qt.transparent)

            painter = QPainter(pixmap)
            painter.setPen(QColor(229, 227, 221))
            font = QFont("Cascadia Mono", 14)
            painter.setFont(font)
            painter.translate(label.width() / 2, label.height() / 2)
            painter.rotate(90)  # Rotate by -90 degrees
            painter.drawText(-250, 5, text)
            painter.end()

            label.setPixmap(pixmap)
    def seeTreePic(self,time):
        # iqTree.tree()
        self.Tree = treeUI.Stats(time)
        self.Tree.ui.show()
    def FastTree(self,time):
        mods=self.ui.mods.currentText()
        if mods=="GTR":
            Fasttree.tree(time,"-gtr -nt")
        elif mods=="JTT":
            Fasttree.tree(time,"")
        elif mods=="LG":
            Fasttree.tree(time,"-lg")
        elif mods=="WAG":
            Fasttree.tree(time,"-wag")
        QMessageBox().about(self.ui, "successful", "Generating the Evolutionary Tree successfully!")
    def modelFinder(self,time):
        model_finder.tree(time,'','')
        QMessageBox().about(self.ui, "successful", "Successfully find the optimal model!")
# app = QApplication([])
# stats = Stats('2024-03-27-16-29-39',['Citrus × aurantium', 'Sapindus mukorossi', 'Arctium lappa', 'Vitis vinifera'])
# stats.ui.show()
# app.exec()