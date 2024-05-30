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
        self.ui = QUiLoader().load('ui/IQ-Tree.ui')
        self.setRotatedLabel('IQ-TREE')
        self.combobox = self.ui.iqGroupSelect
        self.model = QStandardItemModel()
        for item_text in select:
            item = QStandardItem(item_text)
            item.setCheckable(True)
            item.setCheckState(Qt.Unchecked)
            self.model.appendRow(item)
        self.combobox.setModel(self.model)
        self.combobox.view().viewport().installEventFilter(self)
        self.combobox.view().pressed.connect(self.handle_item_pressed)
        self.ui.iqtree.clicked.connect(lambda:self.iqTree(time))
        self.ui.pic.clicked.connect(lambda:self.seeTreePic(time))

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

    def iqTree(self, time):
        selected_items = []
        for index in range(self.model.rowCount()):
            item = self.model.item(index)
            if item.checkState() == Qt.Checked:
                txt = item.text().replace(' ', '_')
                selected_items.append(txt)
        str = selected_items
        outGroup = ','.join(str)
        bootSelect = self.ui.bootSelect.currentText()
        modSelect = self.ui.mod.text()
        num = self.ui.iqNum.text()

        if outGroup == '':
            if bootSelect == 'Ultrafast':
                if modSelect == "AUTO":
                    iqTree.tree(time, "", f"-bb {num}", "", "-redo")
                else:
                    iqTree.tree(time, "", f"-bb {num}", "-m", f"{modSelect} -redo")
            elif bootSelect == 'Standard':
                if modSelect == "AUTO":
                    iqTree.tree(time, f"-b {num}", "", "", "-redo")
                else:
                    iqTree.tree(time, f"-b {num}", "", "-m", f"{modSelect} -redo")
            elif bootSelect == 'None':
                if modSelect == "AUTO":
                    iqTree.tree(time, "", "", "", "-redo")
                else:
                    iqTree.tree(time, "", "", "-m", f"{modSelect} -redo")
        else:
            if bootSelect == 'Ultrafast':
                if modSelect == "AUTO":
                    iqTree.tree(time, "", f"-bb {num}", "-o", f"{outGroup} -redo")
                else:
                    iqTree.tree(time, "", f"-bb {num}", "-o", f"{outGroup} -m {modSelect} -redo")
            elif bootSelect == 'Standard':
                if modSelect == 'AUTO':
                    iqTree.tree(time, f"-b {num}", "", "-o", f"{outGroup} -redo")
                else:
                    iqTree.tree(time, f"-b {num}", "", "-o", f"{outGroup} -m {modSelect} -redo")
            elif bootSelect == 'None':
                if modSelect == "AUTO":
                    iqTree.tree(time, "", "", "-o", f"{outGroup} -redo")
                else:
                    iqTree.tree(time, "", "", "-o", f"{outGroup} -m {modSelect} -redo")
        QMessageBox().about(self.ui, "successful", "Generating the Evolutionary Tree successfully!")


    def eventFilter(self, object, event):
        if event.type() == QEvent.MouseButtonRelease:
            if self.combobox.view().rect().contains(event.pos()):
                index = self.combobox.view().indexAt(event.pos())
                item = self.model.itemFromIndex(index)
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