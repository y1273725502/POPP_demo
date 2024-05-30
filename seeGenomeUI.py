import pandas as pd
from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QTableWidgetItem, QFileDialog
import pandas.io.formats.excel
pandas.io.formats.excel.header_style = None

work_fold = ""

class Stats:
    def __init__(self,allgenes,spec,dict):
        super().__init__()
        self.ui = QUiLoader().load('ui/seeAllGenome.ui')
        self.ui.workFolder.clicked.connect(self.work_folder)
        self.ui.execl.clicked.connect(self.execl)
        table=self.ui.table
        # 设置行数
        table.setRowCount(len(spec))
        # 设置列数
        table.setColumnCount(len(allgenes))
        table.setHorizontalHeaderLabels(allgenes)  # 设置列标题
        for row, species in enumerate(spec):
            table.setVerticalHeaderItem(row, QTableWidgetItem(species))
            for i, gen in enumerate(allgenes):
                for col, gene in enumerate(dict[species]):
                    if gen == gene:
                        item = QTableWidgetItem()
                        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)  # 设置单元格为不可编辑
                        item.setCheckState(QtCore.Qt.Checked)
                        table.setItem(row, i, item)
                        break
                    else:
                        item = QTableWidgetItem()
                        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)  # 设置单元格为不可编辑
                        item.setCheckState(QtCore.Qt.Unchecked)
                        table.setItem(row, i, item)


    def work_folder(self):
        global work_fold
        work_fold = QFileDialog.getExistingDirectory(self.ui, "选择文件夹")

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