import os
import shutil
import sqlite3
from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QFileDialog, QTreeWidgetItem

import Muscle
import clustal
import conservedSequence
import filter_mitochondrial
import findAllGene
import geneForEachSpec
import geneToFolder
import mafftWay
import seeAlignRes
import seeGenomeUI
import tax_info_mitochondrial
import toTreeUI
import trimal
from download_file import download_file
from split_to_fasta import split_to_fasta

work_fold = ""
selection = []
# 获取当前日期和时间
now = datetime.now()
# 格式化日期和时间的输出
date_time = now.strftime("%Y-%m-%d-%H-%M-%S")
# 创建文件夹名
folder_name = f"{date_time}"
# 检查文件夹是否已存在，如果没有则创建新文件夹
if not os.path.exists(folder_name):
    os.mkdir(folder_name)


class Stats:

    def __init__(self):
        self.levels = ["orgGroup", "orgClass", "orgOrder", "family", "genus", "orgName"]
        self.conn = sqlite3.connect('mitochondrion_species_nc.db')
        self.cursor = self.conn.cursor()
        self.ui = QUiLoader().load('ui/mitochondrion.ui')
        self.ui.read.clicked.connect(self.read)
        self.ui.pair.clicked.connect(self.pair)
        self.ui.newSpec.clicked.connect(self.upload)
        self.ui.download.clicked.connect(self.download)
        self.ui.downloadSelected.clicked.connect(self.download_selected_file)
        self.ui.treeWidget.itemExpanded.connect(self.handleExpanded)
        self.ui.treeWidget.itemChanged.connect(self.handleItemChanged)
        self.fill_top_tree_widget()
        self.ui.folder.clicked.connect(self.choose_folder)
        self.ui.selection.clicked.connect(self.selection)
        self.ui.showSelection.clicked.connect(self.showSelection)
        self.ui.deleteSelection.clicked.connect(self.deleteSelection)
        self.ui.split.clicked.connect(self.split_gene)
        self.ui.pairRes.clicked.connect(self.pairRes)
        self.ui.seeAlignRes.clicked.connect(self.seeAlignRes)
        self.ui.editTree.clicked.connect(self.seeTree)
        self.ui.setStyleSheet("""
                    /* 设置整体背景颜色 */
                    QWidget {
                        background-color: #F0F0F0; /* 用你喜欢的颜色替换这里的值 */
                    }

                    /* 设置按钮的样式 */
                    QPushButton {
                        background-color: #4CAF50; /* 按钮正常状态的背景颜色 */
                        color: white; /* 按钮正常状态的文字颜色 */
                        border: 1px solid #4CAF50; /* 按钮正常状态的边框 */
                        border-radius: 4px; /* 按钮的边角弧度 */
                        padding: 5px 10px; /* 按钮文字和边框的内边距 */
                    }

                    QPushButton:hover {
                        background-color: #45a049; /* 鼠标悬停在按钮上时的背景颜色 */
                    }

                    QPushButton:pressed {
                        background-color: #349946; /* 按钮被按下时的背景颜色 */
                    }

                    /* 设置文本框的样式 */
                    QLineEdit {
                        background-color: white; /* 文本框的背景颜色 */
                        border: 1px solid #ccc; /* 文本框的边框 */
                        border-radius: 4px; /* 文本框的边角弧度 */
                        padding: 2px 5px; /* 文本框文字和边框的内边距 */
                    }

                    /* 设置下拉框的样式 */
                    QComboBox {
                        background-color: white; /* 下拉框的背景颜色 */
                        border: 1px solid #ccc; /* 下拉框的边框 */
                        border-radius: 4px; /* 下拉框的边角弧度 */
                        padding: 2px 5px; /* 下拉框文字和边框的内边距 */
                    }
                """)


    def seeTree(self):
        self.toTree = toTreeUI.Stats(date_time,selection)
        self.toTree.ui.show()

    def seeAlignRes(self):
        self.seealignRes = seeAlignRes.Stats(date_time)
        self.seealignRes.ui.show()

    def pairRes(self):
        pairWay = self.ui.pairWay.currentText()
        conserved_sequence = conservedSequence.conservedSequence(selection, work_fold,'mitochondrion_species_nc.db')
        if pairWay == 'MAFFT':
            for gene in conserved_sequence:
                mafftWay.mafftWay(date_time, gene)
                trimal.trimAl(date_time,gene)
            split_to_fasta(date_time,selection,conserved_sequence)

        elif pairWay == 'ClustalW':
            for gene in conserved_sequence:
                clustal.clustal(date_time,gene)
                trimal.trimAl(date_time, gene)
            split_to_fasta(date_time, selection, conserved_sequence)

        elif pairWay == 'Muscle':
            for gene in conserved_sequence:
                Muscle.muscle(date_time,gene)
                trimal.trimAl(date_time, gene)
            split_to_fasta(date_time, selection, conserved_sequence)

    def split_gene(self):
        allSequences = findAllGene.findAllGene(selection, work_fold,'mitochondrion_species_nc.db')
        geneToFolder.geneToFolder(allSequences, selection, work_fold, date_time,'mitochondrion_species_nc.db')
    def deleteSelection(self):
        global selection
        selection = []
    def showSelection(self):
        allSequences = findAllGene.findAllGene(selection, work_fold,'mitochondrion_species_nc.db')
        dict = geneForEachSpec.geneForEachSpec(selection, work_fold,'mitochondrion_species_nc.db')
        self.show_selection = seeGenomeUI.Stats(allSequences, selection, dict)
        self.show_selection.ui.show()
    def selection(self):
        # 使用案例
        global selection
        selected_leaf_items = self.get_checked_leaf_items()
        for item in selected_leaf_items:
            selection.append(item.text(0))
        print(selection)
    def choose_folder(self):
        global work_fold
        work_fold = QFileDialog.getExistingDirectory(self.ui, "选择文件夹")

    def handleItemChanged(self, item, column):  # 选择父节点，自动选择所有子节点
        if item.isDisabled():
            return
        if item.checkState(column) == Qt.Checked:
            for i in range(item.childCount()):
                item.child(i).setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.child(i).setCheckState(0, Qt.Checked)
        elif item.checkState(column) == Qt.Unchecked:
            for i in range(item.childCount()):
                item.child(i).setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.child(i).setCheckState(0, Qt.Unchecked)

    def handleExpanded(self, item):
        if item.childCount() > 0:  # Avoids duplicates if item is expanded multiple times
            return

        parent_level_index = item.data(1, Qt.UserRole)
        if parent_level_index >= len(self.levels) - 1:
            return  # This item is a leaf node.

        parent_level_name = self.levels[parent_level_index]
        parent_name = item.text(0)

        # Get the children for this item from the database
        children = self.get_children(parent_level_name, parent_name)
        for child_name in children:
            child_item = QTreeWidgetItem(item)
            child_item.setText(0, child_name)
            child_item.setCheckState(0, Qt.Unchecked)
            child_item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
            child_item.setData(1, Qt.UserRole, parent_level_index + 1)

    def fill_top_tree_widget(self):
        query = "SELECT distinct orgGroup FROM organisms"
        self.cursor.execute(query)
        orgGroups = self.cursor.fetchall()

        for orgGroup in orgGroups:
            top_item = QTreeWidgetItem(self.ui.treeWidget)
            top_item.setText(0, orgGroup[0])
            top_item.setCheckState(0, Qt.Unchecked)
            top_item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
            top_item.setData(1, Qt.UserRole, 0)

            children = self.get_children("orgGroup", orgGroup[0])
            for child_name in children:
                child_item = QTreeWidgetItem(top_item)
                child_item.setText(0, child_name)
                child_item.setCheckState(0, Qt.Unchecked)
                child_item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
                child_item.setData(1, Qt.UserRole, 1)

    def get_children(self, parent_level_name, parent_name):
        child_level_name = self.levels[self.levels.index(parent_level_name) + 1]
        query = f"SELECT DISTINCT {child_level_name} from organisms WHERE {parent_level_name} == '{parent_name}'"
        self.cursor.execute(query)
        children = self.cursor.fetchall()
        return [child[0] for child in children]

    def get_checked_leaf_items(self):
        def iterate(item):
            checked_leaf_items = []
            for i in range(item.childCount()):
                child = item.child(i)
                if child.childCount() == 0 and child.checkState(0) == Qt.Checked:  # 检查叶节点是否已勾选
                    checked_leaf_items.append(child)
                else:
                    checked_leaf_items.extend(iterate(child))  # 递归检查
            return checked_leaf_items

        root_item = self.ui.treeWidget.invisibleRootItem()
        checked_leaf_items = iterate(root_item)
        return checked_leaf_items

    def download_selected_file(self):
        # 使用案例
        selected_leaf_items = self.get_checked_leaf_items()
        for item in selected_leaf_items:
            print(item.text(0))
        for item in selected_leaf_items:
            # 连接到SQLite数据库
            conn = sqlite3.connect('mitochondrion_species_nc.db')
            cursor = conn.cursor()
            # 执行查询语句，获取"nc"列和"species"列的全部行
            query = f"SELECT * FROM organisms WHERE orgName = '{item.text(0)}'"
            cursor.execute(query)
            # 获取查询结果
            rows = cursor.fetchall()
            # 关闭连接
            conn.close()
            try:
                print(rows[0][1])
            except IndexError:
                print("No organism")
            if os.path.exists(work_fold + "/" + rows[0][1] + ".txt"):
                print("下载的文件已存在")
                continue
            else:
                print("下载中")
                genbank_id = rows[0][1]
                download_file(genbank_id, work_fold)

    def download(self):
        # 连接到SQLite数据库
        conn = sqlite3.connect('mitochondrion_species_nc.db')
        cursor = conn.cursor()
        # 执行查询语句，获取"nc"列和"species"列的全部行
        query = "SELECT * FROM organisms"
        cursor.execute(query)
        # 获取查询结果
        rows = cursor.fetchall()
        # 关闭连接
        conn.close()
        for species in rows:
            print(species[1])

        folder = QFileDialog.getExistingDirectory(self.ui, "选择文件夹")
        for species in rows:
            if os.path.exists(folder + "/" + species[1] + ".txt"):
                pass
            else:
                genbank_id = species[1]
                download_file(genbank_id, folder)

    def pair(self):
        # 连接到SQLite数据库
        conn = sqlite3.connect('mitochondrion_species_nc.db')
        cursor = conn.cursor()
        # 执行查询语句，获取"nc"列和"species"列的全部行
        query = "SELECT * FROM SpeciesNC"
        cursor.execute(query)
        # 获取查询结果
        rows = cursor.fetchall()
        # 关闭连接
        conn.close()
        for species in rows:
            print(species[1])
            tax_info_mitochondrial.tax_info(species[0],species[1], "mitochondrion_species_nc.db")

    def read(self):
        print("请选择nuccore_result.txt")
        fold,_ = QFileDialog.getOpenFileName(self.ui, "选择nuccore_result.txt")
        print(fold)
        filter_mitochondrial.filter_mitochondrial(fold)

    def upload(self):
        fold = QFileDialog.getExistingDirectory(self.ui, "选择文件夹")
        if fold is not None:
            name=self.ui.uploadName.currentText()
            id=self.ui.uploadID.currentText()

            shutil.copy(fold, f"{work_fold}/{id}.txt")

            # 创建一个数据库连接
            conn = sqlite3.connect('mitochondrion_species_nc.db')

            # 创建一个游标对象
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO SpeciesNC (species, nc)
                VALUES (?, ?)
            ''', (name, id))

            # 创建一个游标对象
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO organisms VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                      (name, id, "upload", "upload", "upload", "upload", "upload", "upload"))
            # 提交更改并关闭连接
            conn.commit()
            conn.close()

            print("导入成功！请重启应用")




# app = QApplication([])
# stats = Stats()
# stats.ui.show()
# app.exec()
