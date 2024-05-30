import os

from PySide6.QtCore import Qt, QEvent, QTimer
from PySide6.QtGui import QStandardItemModel, QStandardItem, QPixmap, QPainter, QColor, QFont
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QComboBox, QMainWindow, QApplication, QLabel

import Fasttree
import finderRes
import iqTree
import model_finder
import mrbayes
import treeUI


class Stats(QMainWindow):
    def __init__(self,time,select):
        super().__init__()
        self.ui = QUiLoader().load('ui/toTree.ui')
        self.setRotatedLabel('Tree editing')
        # 创建 QTimer 对象，设置长按时间为1000ms
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.on_long_press)
        # 获取界面中的QComboBox
        self.combobox = self.ui.iqGroupSelect
        self.combobox2=self.ui.modelfinder
        self.combobox3=self.ui.mbout


        # 定义自己的Model
        self.model = QStandardItemModel()
        for item_text in select:
            item = QStandardItem(item_text)
            item.setCheckable(True)
            item.setCheckState(Qt.Unchecked)
            self.model.appendRow(item)

        self.model2 = QStandardItemModel()
        for item_text in select:
            item = QStandardItem(item_text)
            item.setCheckable(True)
            item.setCheckState(Qt.Unchecked)
            self.model2.appendRow(item)

        self.model3 = QStandardItemModel()
        for item_text in select:
            item = QStandardItem(item_text)
            item.setCheckable(True)
            item.setCheckState(Qt.Unchecked)
            self.model3.appendRow(item)

        # 使用自定义的Model替换原先的Model
        self.combobox.setModel(self.model)
        self.combobox2.setModel(self.model2)
        self.combobox3.setModel(self.model3)
        # 给QComboBox的视图安装事件过滤器，注意这里已经把self传入了
        self.combobox.view().viewport().installEventFilter(self)
        self.combobox2.view().viewport().installEventFilter(self)
        self.combobox3.view().viewport().installEventFilter(self)
        # 绑定点击事件
        self.combobox.view().pressed.connect(self.handle_item_pressed)
        self.combobox2.view().pressed.connect(self.handle_item_pressed_2)
        self.combobox3.view().pressed.connect(self.handle_item_pressed_3)

        self.ui.iqtree.clicked.connect(lambda:self.iqTree(time))
        self.ui.fasttree.clicked.connect(lambda:self.FastTree(time))
        self.ui.pic.clicked.connect(lambda:self.seeTreePic(time))
        self.ui.modelfinder_button.clicked.connect(lambda:self.modelFinder(time))
        self.ui.model_results.clicked.connect(lambda:self.seeFinderRes(time))
        self.ui.mrbayes.clicked.connect(lambda: self.mrbayes(time))

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
    def returnMain(self):
        self.ui.close()
    def on_long_press(self):
        self.timer.stop()  # 停止计时器
        print("Button has been long pressed")
        self.ui.showMinimized()  # 长按后最小化窗口

    def modelFinder(self,time):
        selected_items=[]
        for index in range(self.model2.rowCount()):
            item = self.model2.item(index)
            if item.checkState() == Qt.Checked:
                txt=item.text().replace(' ','_')
                selected_items.append(txt)
        str=selected_items
        outGroup = ','.join(str)
        if outGroup=='':
            model_finder.tree(time,'','')
        else:
            model_finder.tree(time,"-o",f'{outGroup} -redo')

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

    def iqTree(self,time):
        selected_items = []
        for index in range(self.model.rowCount()):
            item = self.model.item(index)
            if item.checkState() == Qt.Checked:
                txt=item.text().replace(' ','_')
                selected_items.append(txt)
        str=selected_items
        outGroup = ','.join(str)
        bootSelect = self.ui.bootSelect.currentText()
        modSelect=self.ui.mod.text()
        num = self.ui.iqNum.text()

        if outGroup=='':
            if bootSelect=='Ultrafast':
                if modSelect=="AUTO":
                    iqTree.tree(time,"",f"-bb {num}","","-redo")
                else:
                    iqTree.tree(time,"",f"-bb {num}","-m",f"{modSelect} -redo")
            elif bootSelect=='Standard':
                if modSelect=="AUTO":
                    iqTree.tree(time,f"-b {num}","","","-redo")
                else:
                    iqTree.tree(time, f"-b {num}", "", "-m",f"{modSelect} -redo")
            elif bootSelect=='None':
                if modSelect=="AUTO":
                    iqTree.tree(time,"","","","-redo")
                else:
                    iqTree.tree(time, "", "", "-m", f"{modSelect} -redo")
        else:
            if bootSelect=='Ultrafast':
                if modSelect=="AUTO":
                    iqTree.tree(time,"",f"-bb {num}","-o",f"{outGroup} -redo")
                else:
                    iqTree.tree(time, "", f"-bb {num}", "-o", f"{outGroup} -m {modSelect} -redo")
            elif bootSelect == 'Standard':
                if modSelect=='AUTO':
                    iqTree.tree(time, f"-b {num}", "", "-o", f"{outGroup} -redo")
                else:
                    iqTree.tree(time, f"-b {num}", "", "-o", f"{outGroup} -m {modSelect} -redo")
            elif bootSelect == 'None':
                if modSelect=="AUTO":
                    iqTree.tree(time, "", "", "-o", f"{outGroup} -redo")
                else:
                    iqTree.tree(time, "", "", "-o", f"{outGroup} -m {modSelect} -redo")

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

# app = QApplication([])
# stats = Stats('2024-02-16-19-58-04',['Citrus × aurantium', 'Sapindus mukorossi', 'Arctium lappa', 'Vitis vinifera'])
# stats.ui.show()
# app.exec()
