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
import nj_tree
import treeUI
class Stats(QMainWindow):
    def __init__(self,time,select):
        super().__init__()
        self.ui = QUiLoader().load('ui/nj_tree.ui')
        self.setRotatedLabel('NJ_TREE')
        self.ui.njtree.clicked.connect(lambda:self.njTreePic(time))
        self.ui.pic.clicked.connect(lambda:self.seeTreePic(time))
    def njTreePic(self,time):
        nj_tree.nj_Tree(time)
        QMessageBox().about(self.ui, "successful", "Generating the Evolutionary Tree successfully!")
    def seeTreePic(self,time):
        # iqTree.tree()
        self.Tree = treeUI.Stats(time)
        self.Tree.ui.show()
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