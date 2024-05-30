import datetime
import os
import sqlite3
import time

from PySide6 import QtCore
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QLabel, QFrame, QTreeWidgetItem, QMessageBox
from PySide6.QtGui import QPainter, QPixmap, QColor, QFont
from PySide6.QtCore import Qt, QTimer

import ch_find_pair_species
import ch_next
import ch_speciesManage
import findAllGene
import geneForEachSpec
import geneToFolder
import mi_find_pair_species
import mi_next
import mi_speciesManage
import ch_viewAllGenome
import mi_viewAllGenome
from download_file import download_file
from PySide6.QtGui import QIcon

fold = os.getcwd()
ch_cds = f"{fold}/chloroplast_cds"
mi_cds = f"{fold}/mitochondrial_cds"
ch_selection = []
mi_selection = []


class Stats:
    def __init__(self):
        super().__init__()
        self.ch_levels = ["kingdom", "phylum", "class", "Orderr", "family", "genus", "species"]
        self.ch_conn = sqlite3.connect('chloroplast_species_nc.db')
        self.ch_cursor = self.ch_conn.cursor()
        self.mi_levels = ["kingdom", "phylum", "class", "Orderr", "family", "genus", "species"]
        self.mi_conn = sqlite3.connect('mitochondrion_species_nc.db')
        self.mi_cursor = self.mi_conn.cursor()

        self.ui = QUiLoader().load('ui/start.ui')
        self.setRotatedLabel('Plant phylogenetic analysis platform')
        icon = QIcon("059.png")
        self.bu=self.ui.ch_manage
        self.bu.setIcon(icon)
        self.bu.setIconSize(QtCore.QSize(32, 32))

        icon = QIcon("059_添加.png")
        self.bu = self.ui.ch_add
        self.bu.setIcon(icon)
        self.bu.setIconSize(QtCore.QSize(32, 32))

        icon = QIcon("059_减少.png")
        self.bu = self.ui.ch_remove
        self.bu.setIcon(icon)
        self.bu.setIconSize(QtCore.QSize(32, 32))

        icon = QIcon("059_搜索.png")
        self.bu = self.ui.ch_view
        self.bu.setIcon(icon)
        self.bu.setIconSize(QtCore.QSize(32, 32))

        icon = QIcon("059_走势.png")
        self.bu = self.ui.ch_next
        self.bu.setIcon(icon)
        self.bu.setIconSize(QtCore.QSize(32, 32))

        icon = QIcon("059.png")
        self.bu=self.ui.mi_manage
        self.bu.setIcon(icon)
        self.bu.setIconSize(QtCore.QSize(32, 32))

        icon = QIcon("059_添加.png")
        self.bu = self.ui.mi_add
        self.bu.setIcon(icon)
        self.bu.setIconSize(QtCore.QSize(32, 32))

        icon = QIcon("059_减少.png")
        self.bu = self.ui.mi_remove
        self.bu.setIcon(icon)
        self.bu.setIconSize(QtCore.QSize(32, 32))

        icon = QIcon("059_搜索.png")
        self.bu = self.ui.mi_view
        self.bu.setIcon(icon)
        self.bu.setIconSize(QtCore.QSize(32, 32))

        icon = QIcon("059_走势.png")
        self.bu = self.ui.mi_next
        self.bu.setIcon(icon)
        self.bu.setIconSize(QtCore.QSize(32, 32))



        self.ui.ch_tree.itemExpanded.connect(self.ch_handleExpanded)
        self.ui.ch_tree.itemChanged.connect(self.ch_handleItemChanged)
        self.ch_fill_top_tree_widget()
        self.ui.mi_tree.itemExpanded.connect(self.mi_handleExpanded)
        self.ui.mi_tree.itemChanged.connect(self.mi_handleItemChanged)
        self.mi_fill_top_tree_widget()
        self.ui.ch_remove.clicked.connect(self.deleteSelection)
        self.ui.mi_remove.clicked.connect(self.deleteSelection)
        self.ui.ch_manage.clicked.connect(self.ch_manage)
        self.ui.mi_manage.clicked.connect(self.mi_manage)
        self.ui.ch_view.clicked.connect(self.ch_showSelection)
        self.ui.mi_view.clicked.connect(self.mi_showSelection)
        self.ui.mi_add.clicked.connect(self.mi_selection)
        self.ui.ch_add.clicked.connect(self.ch_selection)
        self.ui.ch_next.clicked.connect(self.ch_next)
        self.ui.mi_next.clicked.connect(self.mi_next)

    def ch_next(self):

        self.ch_download_selected_file()
        # 获取当前日期和时间
        now = datetime.datetime.now()
        # 格式化日期和时间的输出
        date_time = now.strftime("%Y-%m-%d-%H-%M-%S")
        # 创建文件夹名
        folder_name = f"{date_time}"
        # 检查文件夹是否已存在，如果没有则创建新文件夹
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        allSequences = findAllGene.findAllGene(ch_selection, ch_cds, 'chloroplast_species_nc.db')
        geneToFolder.geneToFolder(allSequences, ch_selection, ch_cds, folder_name, 'chloroplast_species_nc.db')

        # mi_spe=ch_find_pair_species.findPairSpecies(ch_selection)
        # if mi_spe==None:
        #     pass
        # else:
        #     # 创建消息框
        #     message_box = QMessageBox()
        #
        #     # 设置消息框的标题和文本内容
        #     message_box.setWindowTitle("The mitochondria of the same name were found")
        #     message_box.setText("Simultaneous mitochondrial and chloroplast building operations will be performed")
        #
        #     # 添加一个按钮，用于关闭提示框
        #     message_box.addButton(QMessageBox.Ok)
        #
        #     # 显示消息框
        #     message_box.exec()
        #     time.sleep(1)
        #     global mi_selection
        #     mi_selection=mi_spe
        #     self.mi_next_2()

        self.next = ch_next.Stats(folder_name, ch_selection, fold)
        self.next.ui.show()

    # def ch_next_2(self):
    #     self.ch_download_selected_file()
    #     # 获取当前日期和时间
    #     now = datetime.datetime.now()
    #     # 格式化日期和时间的输出
    #     date_time = now.strftime("%Y-%m-%d-%H-%M-%S")
    #     # 创建文件夹名
    #     folder_name = f"{date_time}"
    #     # 检查文件夹是否已存在，如果没有则创建新文件夹
    #     if not os.path.exists(folder_name):
    #         os.mkdir(folder_name)
    #     allSequences = findAllGene.findAllGene(ch_selection, ch_cds, 'chloroplast_species_nc.db')
    #     geneToFolder.geneToFolder(allSequences, ch_selection, ch_cds,folder_name, 'chloroplast_species_nc.db')
    #
    #
    #     self.next = ch_next.Stats(folder_name,ch_selection,fold)
    #     self.next.ui.move(200,200)
    #     self.next.ui.show()
    def mi_next(self):
        self.mi_download_selected_file()
        # 获取当前日期和时间
        now = datetime.datetime.now()
        # 格式化日期和时间的输出
        date_time = now.strftime("%Y-%m-%d-%H-%M-%S")
        # 创建文件夹名
        folder_name = f"{date_time}"
        # 检查文件夹是否已存在，如果没有则创建新文件夹
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        allSequences = findAllGene.findAllGene(mi_selection, mi_cds, 'mitochondrion_species_nc.db')
        geneToFolder.geneToFolder(allSequences, mi_selection, mi_cds, folder_name, 'mitochondrion_species_nc.db')

        # ch_spe=mi_find_pair_species.findPairSpecies(mi_selection)
        # if ch_spe==None:
        #     pass
        # else:
        #     # 创建消息框
        #     message_box = QMessageBox()
        #
        #     # 设置消息框的标题和文本内容
        #     message_box.setWindowTitle("The chloroplast of the same name were found")
        #     message_box.setText("Simultaneous mitochondrial and chloroplast building operations will be performed")
        #
        #     # 添加一个按钮，用于关闭提示框
        #     message_box.addButton(QMessageBox.Ok)
        #
        #     # 显示消息框
        #     message_box.exec()
        #     time.sleep(1)
        #     global ch_selection
        #     ch_selection=ch_spe
        #     self.ch_next_2()

        self.next = mi_next.Stats(folder_name, mi_selection, fold)

        self.next.ui.show()

    # def mi_next_2(self):
    #     self.mi_download_selected_file()
    #     # 获取当前日期和时间
    #     now = datetime.datetime.now()
    #     # 格式化日期和时间的输出
    #     date_time = now.strftime("%Y-%m-%d-%H-%M-%S")
    #     # 创建文件夹名
    #     folder_name = f"{date_time}"
    #     # 检查文件夹是否已存在，如果没有则创建新文件夹
    #     if not os.path.exists(folder_name):
    #         os.mkdir(folder_name)
    #     allSequences = findAllGene.findAllGene(mi_selection, mi_cds, 'mitochondrion_species_nc.db')
    #     geneToFolder.geneToFolder(allSequences, mi_selection, mi_cds, folder_name, 'mitochondrion_species_nc.db')
    #
    #
    #     self.next = mi_next.Stats(folder_name,mi_selection,fold)
    #     self.next.ui.move(200,200)
    #     self.next.ui.show()

    def mi_download_selected_file(self):
        # 使用案例
        selected_leaf_items = self.mi_get_checked_leaf_items()
        for item in selected_leaf_items:
            print(item.text(0))
        for item in selected_leaf_items:
            # 连接到SQLite数据库
            conn = sqlite3.connect('mitochondrion_species_nc.db')
            cursor = conn.cursor()
            # 执行查询语句，获取"nc"列和"species"列的全部行
            query = f"SELECT * FROM Species WHERE name = '{item.text(0)}'"
            cursor.execute(query)
            # 获取查询结果
            rows = cursor.fetchall()
            # 关闭连接
            conn.close()
            try:
                print(rows[0][1])
            except IndexError:
                print("No organism")
            if os.path.exists(fold + "/mitochondrial_cds/" + rows[0][1] + ".txt"):
                print("下载的文件已存在")
                continue
            else:
                print("下载中")
                genbank_id = rows[0][1]
                download_file(genbank_id, fold + "/mitochondrial_cds")

    def ch_download_selected_file(self):
        # 使用案例
        selected_leaf_items = self.ch_get_checked_leaf_items()
        for item in selected_leaf_items:
            print(item.text(0))
        for item in selected_leaf_items:
            # 连接到SQLite数据库
            conn = sqlite3.connect('chloroplast_species_nc.db')
            cursor = conn.cursor()
            # 执行查询语句，获取"nc"列和"species"列的全部行
            query = f"SELECT * FROM Species WHERE name = '{item.text(0)}'"
            cursor.execute(query)
            # 获取查询结果
            rows = cursor.fetchall()
            # 关闭连接
            conn.close()
            try:
                print(rows[0][1])
            except IndexError:
                print("No organism")
            if os.path.exists(fold + "/chloroplast_cds/" + rows[0][1] + ".txt"):
                print("下载的文件已存在")
                continue
            else:
                print("下载中")
                genbank_id = rows[0][1]
                download_file(genbank_id, fold + "/chloroplast_cds")

    def deleteSelection(self):
        global ch_selection
        global mi_selection
        ch_selection = []
        mi_selection = []
        QMessageBox().about(self.ui,"Cleared successfully!",f"Cleared successfully")

    def mi_get_checked_leaf_items(self):
        def iterate(item):
            checked_leaf_items = []
            for i in range(item.childCount()):
                child = item.child(i)
                if child.childCount() == 0 and child.checkState(0) == Qt.Checked:  # 检查叶节点是否已勾选
                    checked_leaf_items.append(child)
                else:
                    checked_leaf_items.extend(iterate(child))  # 递归检查
            return checked_leaf_items

        root_item = self.ui.mi_tree.invisibleRootItem()
        checked_leaf_items = iterate(root_item)
        return checked_leaf_items

    def ch_get_checked_leaf_items(self):
        def iterate(item):
            checked_leaf_items = []
            for i in range(item.childCount()):
                child = item.child(i)
                if child.childCount() == 0 and child.checkState(0) == Qt.Checked:  # 检查叶节点是否已勾选
                    checked_leaf_items.append(child)
                else:
                    checked_leaf_items.extend(iterate(child))  # 递归检查
            return checked_leaf_items

        root_item = self.ui.ch_tree.invisibleRootItem()
        checked_leaf_items = iterate(root_item)
        return checked_leaf_items

    def ch_selection(self):
        # 使用案例
        global ch_selection
        selected_leaf_items = self.ch_get_checked_leaf_items()
        for item in selected_leaf_items:
            ch_selection.append(item.text(0))
        QMessageBox().about(self.ui,"Add successfully!",f"Current Candidate Genes:{ch_selection}")
        print(ch_selection)

    def mi_selection(self):
        global mi_selection
        selected_leaf_items = self.mi_get_checked_leaf_items()
        for item in selected_leaf_items:
            mi_selection.append(item.text(0))
        QMessageBox().about(self.ui,"Add successfully!",f"Current Candidate Genes:{mi_selection}")
        print(mi_selection)

    def ch_showSelection(self):
        self.ch_download_selected_file()
        allSequences = findAllGene.findAllGene(ch_selection, ch_cds, 'chloroplast_species_nc.db')
        dict = geneForEachSpec.geneForEachSpec(ch_selection, ch_cds, 'chloroplast_species_nc.db')
        # 定义一个自定义的排序函数，按照基因名称的第一个字母排序
        def custom_sort(gene):
            return gene[0]

        # 对基因列表进行排序
        sorted_gene_list = sorted(allSequences, key=custom_sort)
        # 打印排序后的基因列表
        print(sorted_gene_list)
        self.show_selection = ch_viewAllGenome.Stats(sorted_gene_list, ch_selection, dict, ch_selection, ch_cds)
        self.show_selection.ui.show()

    def mi_showSelection(self):
        self.mi_download_selected_file()
        allSequences = findAllGene.findAllGene(mi_selection, mi_cds, 'mitochondrion_species_nc.db')
        dict = geneForEachSpec.geneForEachSpec(mi_selection, mi_cds, 'mitochondrion_species_nc.db')

        # 定义一个自定义的排序函数，按照基因名称的第一个字母排序
        def custom_sort(gene):
            return gene[0]

        # 对基因列表进行排序
        sorted_gene_list = sorted(allSequences, key=custom_sort)
        # 打印排序后的基因列表
        print(sorted_gene_list)
        self.show_selection = mi_viewAllGenome.Stats(sorted_gene_list, mi_selection, dict, mi_selection, mi_cds)
        self.show_selection.ui.show()

    def mi_handleItemChanged(self, item, column):  # 选择父节点，自动选择所有子节点
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

    def mi_handleExpanded(self, item):
        if item.childCount() > 0:  # Avoids duplicates if item is expanded multiple times
            return

        parent_level_index = item.data(1, Qt.UserRole)
        if parent_level_index >= len(self.mi_levels) - 1:
            return  # This item is a leaf node.

        parent_level_name = self.mi_levels[parent_level_index]
        parent_name = item.text(0)

        # Get the children for this item from the database
        children = self.mi_get_children(parent_level_name, parent_name)
        if children:  # only show arrow if there are children
            item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
        for child_name in children:
            child_item = QTreeWidgetItem(item)
            child_item.setText(0, child_name)
            child_item.setCheckState(0, Qt.Unchecked)
            child_item.setData(1, Qt.UserRole, parent_level_index + 1)
            if self.mi_get_children(self.ch_levels[parent_level_index + 1], child_name):
                child_item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)

    def mi_fill_top_tree_widget(self):
        query = "SELECT distinct kingdom FROM Species"
        self.mi_cursor.execute(query)
        kingdom = self.mi_cursor.fetchall()

        for orgGroup in kingdom:
            top_item = QTreeWidgetItem(self.ui.mi_tree)
            top_item.setText(0, orgGroup[0])
            top_item.setCheckState(0, Qt.Unchecked)
            top_item.setData(1, Qt.UserRole, 0)

            children = self.mi_get_children("kingdom", orgGroup[0])
            if children:  # only show arrow if there are children
                top_item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
            for child_name in children:
                child_item = QTreeWidgetItem(top_item)
                child_item.setText(0, child_name)
                child_item.setCheckState(0, Qt.Unchecked)
                child_item.setData(1, Qt.UserRole, 1)
                if self.mi_get_children("phylum", child_name):  # replace "phylum" with the actual level name
                    child_item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)

    def mi_get_children(self, parent_level_name, parent_name):
        parent_level_index = self.mi_levels.index(parent_level_name)
        if parent_level_index >= len(self.mi_levels) - 1:  # if this is the last level
            return []  # return an empty list because there are no children
        child_level_name = self.mi_levels[parent_level_index + 1]
        query = f"SELECT DISTINCT {child_level_name} from Species WHERE {parent_level_name} == '{parent_name}'"
        self.mi_cursor.execute(query)
        children = self.mi_cursor.fetchall()
        return [child[0] for child in children]

    def ch_handleItemChanged(self, item, column):  # 选择父节点，自动选择所有子节点
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

    def ch_handleExpanded(self, item):
        if item.childCount() > 0:  # Avoids duplicates if item is expanded multiple times
            return

        parent_level_index = item.data(1, Qt.UserRole)
        if parent_level_index >= len(self.ch_levels) - 1:
            return  # This item is a leaf node.

        parent_level_name = self.ch_levels[parent_level_index]
        parent_name = item.text(0)

        # Get the children for this item from the database
        children = self.ch_get_children(parent_level_name, parent_name)
        if children:  # only show arrow if there are children
            item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
        for child_name in children:
            child_item = QTreeWidgetItem(item)
            child_item.setText(0, child_name)
            child_item.setCheckState(0, Qt.Unchecked)
            child_item.setData(1, Qt.UserRole, parent_level_index + 1)
            if self.ch_get_children(self.ch_levels[parent_level_index + 1], child_name):
                child_item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)

    def ch_fill_top_tree_widget(self):
        query = "SELECT distinct kingdom FROM Species"
        self.ch_cursor.execute(query)
        kingdom = self.ch_cursor.fetchall()

        for orgGroup in kingdom:
            top_item = QTreeWidgetItem(self.ui.ch_tree)
            top_item.setText(0, orgGroup[0])
            top_item.setCheckState(0, Qt.Unchecked)
            top_item.setData(1, Qt.UserRole, 0)

            children = self.ch_get_children("kingdom", orgGroup[0])
            if children:  # only show arrow if there are children
                top_item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
            for child_name in children:
                child_item = QTreeWidgetItem(top_item)
                child_item.setText(0, child_name)
                child_item.setCheckState(0, Qt.Unchecked)
                child_item.setData(1, Qt.UserRole, 1)
                if self.ch_get_children("phylum", child_name):  # replace "phylum" with the actual level name
                    child_item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)

    def ch_get_children(self, parent_level_name, parent_name):
        parent_level_index = self.ch_levels.index(parent_level_name)
        if parent_level_index >= len(self.ch_levels) - 1:  # if this is the last level
            return []  # return an empty list because there are no children
        child_level_name = self.ch_levels[parent_level_index + 1]
        query = f"SELECT DISTINCT {child_level_name} from Species WHERE {parent_level_name} == '{parent_name}'"
        self.ch_cursor.execute(query)
        children = self.ch_cursor.fetchall()
        return [child[0] for child in children]

    def ch_manage(self):
        self.species_manage = ch_speciesManage.Stats()

        self.species_manage.ui.show()

    def mi_manage(self):
        self.species_manage = mi_speciesManage.Stats()

        self.species_manage.ui.show()

    def on_long_press(self):
        self.timer.stop()  # 停止计时器
        print("Button has been long pressed")
        self.ui.showMinimized()  # 长按后最小化窗口

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


app = QApplication([])
stats = Stats()

stats.ui.show()
app.exec_()
