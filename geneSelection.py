import os
import sqlite3

from PySide6 import QtCore
from PySide6.QtCore import QTimer, Qt, Signal, QObject, QThread
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QLabel, QTableWidgetItem, QMainWindow, QDialog, QApplication, QWidget

import Muscle
import clustal
import conservedSequence
import downloadCompleteGenome
import mafftWay
import seeAlignRes
import toTreeUI
import trimal
from completeGeneToTxt import completeGeneToTxt
from split_to_fasta import split_to_fasta

all_genes_selected = True  # 初始状态下所有基因都被选中
class Stats():
    def __init__(self,conservedGene,fold):

        super(Stats, self).__init__()
        self.ui = QUiLoader().load('ui/GeneSelection.ui')
        self.setRotatedLabel('Gene Selection')
        self.ui.table.setColumnCount(1)
        self.ui.table.setRowCount(len(conservedGene))
        self.ui.table.setHorizontalHeaderLabels(["Genes"])
        self.ui.pushButton.clicked.connect(lambda:self.returnMain(fold))
        for i, gene in enumerate(conservedGene):
            item = QTableWidgetItem(gene)
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            item.setCheckState(Qt.Checked)
            self.ui.table.setItem(i, 0, item)

        # 为"Genes"表头单元格添加点击事件处理函数
        header_item = self.ui.table.horizontalHeaderItem(0)
        header_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # 文本对齐方式
        header_item.setFlags(header_item.flags() | Qt.ItemIsUserCheckable)  # 添加用户可选中标记
        header_item.setCheckState(Qt.Checked if all_genes_selected else Qt.Unchecked)  # 设置初始状态

        def toggle_all_genes_checked(state):
            global all_genes_selected
            all_genes_selected = not all_genes_selected

            for i in range(self.ui.table.rowCount()):
                item = self.ui.table.item(i, 0)
                item.setCheckState(Qt.Checked if all_genes_selected else Qt.Unchecked)

        self.ui.table.horizontalHeader().sectionClicked.connect(toggle_all_genes_checked)



    def name_to_id(self,item, database):
        # 连接到SQLite数据库
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        # 执行查询语句，获取"nc"列和"species"列的全部行
        query = f"SELECT * FROM Species WHERE name = '{item}'"
        cursor.execute(query)
        # 获取查询结果
        rows = cursor.fetchall()
        # 关闭连接
        conn.close()
        return rows[0][1]


    def setRotatedLabel(self, text):
        label = self.ui.findChild(QLabel, 'label')
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

    def detect_checked_rows(self,table):
        checked_rows = []
        for row in range(table.rowCount()):
            item = table.item(row, 0)
            if item is not None and item.checkState() == Qt.Checked:
                checked_rows.append(item.text())
        return checked_rows

    def returnMain(self,fold):
        selected_genes=self.detect_checked_rows(self.ui.table)
        print(selected_genes)
        with open(f"{fold}\\list_file.txt", "w") as file:
            for item in selected_genes:
                file.write(item + "\n")
        self.ui.close()


# app = QApplication([])
# stats = Stats([1,2,3],'/')
#
# stats.ui.show()
# app.exec()