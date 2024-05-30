import pandas as pd
from PySide6 import QtCore
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QColor, QFont, QPainter, QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QTableWidgetItem, QFileDialog, QLabel, QMessageBox
import pandas.io.formats.excel

import conservedSequence

pandas.io.formats.excel.header_style = None


class Stats:
    def __init__(self,allgenes,spec,dict,selection,mi_cds):
        super().__init__()
        self.ui = QUiLoader().load('ui/viewTheGenome.ui')
        self.ui.execl.clicked.connect(self.execl)

        icon = QIcon("059_数据-16.png")
        self.bu = self.ui.execl
        self.bu.setIcon(icon)
        self.bu.setIconSize(QtCore.QSize(32, 32))

        self.setRotatedLabel('View the genomes')
        conserved=conservedSequence.conservedSequence(selection,mi_cds,'mitochondrion_species_nc.db')
        self.ui.label_2.setText(f'There were {len(conserved)} conserved genes')

        table=self.ui.table
        # 设置行数
        table.setRowCount(len(allgenes))  # 将行数设为基因数
        # 设置列数
        table.setColumnCount(len(spec))  # 将列数设为物种数
        table.setHorizontalHeaderLabels(spec)  # 设置水平标题为物种名称
        for row, gene in enumerate(allgenes):
            table.setVerticalHeaderItem(row, QTableWidgetItem(gene))  # 设置垂直标题为基因名称
            for col, species in enumerate(spec):
                for specie_gene in dict.items():
                    if species == specie_gene[0] and gene in specie_gene[1]:
                        item = QTableWidgetItem()
                        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)  # 设置单元格为不可编辑
                        item.setCheckState(QtCore.Qt.Checked)
                        table.setItem(row, col, item)
                        break
                else:
                    item = QTableWidgetItem()
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)  # 设置单元格为不可编辑
                    item.setCheckState(QtCore.Qt.Unchecked)
                    table.setItem(row, col, item)

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
    def returnMain(self):
        self.ui.close()
    def on_long_press(self):
        self.timer.stop()  # 停止计时器
        print("Button has been long pressed")
        self.ui.showMinimized()  # 长按后最小化窗口

    def execl(self):
        rowcount = self.ui.table.rowCount()
        colcount = self.ui.table.columnCount()

        data_for_output = []
        # 添加列标题
        column_headers = ['']  # 首位添加一个空字符串
        column_headers += [self.ui.table.horizontalHeaderItem(col).text() for col in range(colcount)]
        data_for_output.append(column_headers)

        # 补充行标题和列标题
        for row in range(rowcount):
            row_data = []
            # 获取行标题
            row_header = self.ui.table.verticalHeaderItem(row)
            if row_header is not None:
                row_data.append(row_header.text())
            else:
                row_data.append('')

            for col in range(colcount):
                item = self.ui.table.item(row, col)
                if item is not None:
                    if item.checkState() == Qt.Checked:
                        row_data.append('1')  # 根据你的需要更改
                    else:
                        row_data.append('0')  # 根据你的需要更改
                else:
                    row_data.append('')
            data_for_output.append(row_data)

        df = pd.DataFrame(data_for_output)
        writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')
        df.to_excel(writer, index=False, header=False)
        writer.close()
        QMessageBox().about(self.ui, "Successfully exported to Excel!", "Successfully exported to Excel!")