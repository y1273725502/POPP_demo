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
        self.ui = QUiLoader().load('ui/MrBayes.ui')
        self.setRotatedLabel('MrBayes')
        self.combobox3=self.ui.mbout
        self.model3 = QStandardItemModel()
        for item_text in select:
            item = QStandardItem(item_text)
            item.setCheckable(True)
            item.setCheckState(Qt.Unchecked)
            self.model3.appendRow(item)
        self.combobox3.setModel(self.model3)
        self.combobox3.view().viewport().installEventFilter(self)
        self.combobox3.view().pressed.connect(self.handle_item_pressed_3)
        self.ui.mrbayes.clicked.connect(lambda: self.mrbayes(time))
        self.ui.pic.clicked.connect(lambda:self.seeTreePic(time))

    def mrbayes(self,time):
        selected_items = []
        for index in range(self.model3.rowCount()):
            item = self.model3.item(index)
            if item.checkState() == Qt.Checked:
                txt = item.text().replace(' ', '_')
                selected_items.append(txt)
        outgroup = selected_items
        gnum = self.ui.gnum.text()
        SampFreq = self.ui.SampFreq.text()
        printFreq = self.ui.printFreq.text()
        numChains=self.ui.numChains.text()
        mrbayes.tree(time,outgroup,gnum,SampFreq,printFreq,numChains)
        QMessageBox().about(self.ui, "successful", "Generating the Evolutionary Tree successfully!")

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


    def eventFilter(self, object, event):
        if event.type() == QEvent.MouseButtonRelease:
            if self.combobox3.view().rect().contains(event.pos()):
                index = self.combobox3.view().indexAt(event.pos())
                item = self.model3.itemFromIndex(index)
                if item.checkState() == Qt.Checked:
                    item.setCheckState(Qt.Unchecked)
                else:
                    item.setCheckState(Qt.Checked)
                return True
        return False

    def handle_item_pressed(self, index):
        item = self.model.itemFromIndex(index)
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)

    def get_selected_item(self):
        selected_items = []
        for index in range(self.model.rowCount()):
            item = self.model.item(index)
            if item.checkState() == Qt.Checked:
                selected_items.append(item.text())
        print(selected_items)

    def handle_item_pressed_2(self, index):
        item = self.model2.itemFromIndex(index)
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)

    def get_selected_item_2(self):
        selected_items = []
        for index in range(self.model2.rowCount()):
            item = self.model2.item(index)
            if item.checkState() == Qt.Checked:
                selected_items.append(item.text())
        print(selected_items)

    def handle_item_pressed_3(self, index):
        item = self.model3.itemFromIndex(index)
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)

    def get_selected_item_3(self):
        selected_items = []
        for index in range(self.model3.rowCount()):
            item = self.model3.item(index)
            if item.checkState() == Qt.Checked:
                selected_items.append(item.text())
        print(selected_items)

    def seeTreePic(self,time):
        # iqTree.tree()
        self.Tree = treeUI.Stats(time)
        self.Tree.ui.show()