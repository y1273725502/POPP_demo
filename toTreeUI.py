import os

from PySide6.QtCore import Qt, QEvent, QTimer
from PySide6.QtGui import QStandardItemModel, QStandardItem, QPixmap, QPainter, QColor, QFont
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QComboBox, QMainWindow, QApplication, QLabel


import FastTreeUi
import MrBayesUI
import PAML_UI

import iqTreeUI



class Stats(QMainWindow):
    def __init__(self,time,select):
        super().__init__()
        self.ui = QUiLoader().load('ui/method.ui')
        self.setRotatedLabel('Tree method')

        # 获取界面中的QComboBox
        self.combobox = self.ui.method

        self.ui.ok.clicked.connect(lambda:self.ok(time,select))


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

    def ok(self,time,select):
        tree_method=self.combobox.currentText()
        if tree_method=="IQ-TREE":
            iq_tree=iqTreeUI.Stats(time,select)
            iq_tree.ui.show()
        elif tree_method=="ModelFinder+FastTree":
            model_finder=FastTreeUi.Stats(time,select)
            model_finder.ui.show()
        elif tree_method=="MrBayes":
            mr_bayes=MrBayesUI.Stats(time,select)
            mr_bayes.ui.show()
        elif tree_method=="Biopython_nj_tree":
            print("OK")
        elif tree_method=="PAML":
            paml=PAML_UI.Stats(time,select)
            paml.ui.show()
        else:
            print("Invalid")

# app = QApplication([])
# stats = Stats('2024-03-27-16-29-39',['Citrus × aurantium', 'Sapindus mukorossi', 'Arctium lappa', 'Vitis vinifera'])
# stats.ui.show()
# app.exec()
