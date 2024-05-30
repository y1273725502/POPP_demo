import datetime
import os
import sqlite3
import time
import webbrowser

import PySide6
import pandas as pd
from PySide6 import QtCore
from PySide6.QtNetwork import QNetworkCookie
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWebEngineCore import QWebEngineProfile
from PySide6.QtWidgets import QApplication, QLabel, QFrame, QTreeWidgetItem, QMessageBox, QTableWidgetItem, QMainWindow, \
    QGraphicsScene
from PySide6.QtGui import QPainter, QPixmap, QColor, QFont, QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt, QTimer, QUrl, QDateTime, QByteArray
from selenium.webdriver import ActionChains
from PySide6.QtWebEngineCore import QWebEngineCookieStore

import Fasttree
import Muscle
import PAML
import ch_find_pair_species
import ch_next
import ch_speciesManage
import clustal
import conservedSequence
import downloadCompleteGenome
import findAllGene
import geneForEachSpec
import geneSelection
import geneToFolder
import iqTree
import mafftWay
import mi_find_pair_species
import mi_next
import mi_speciesManage
import ch_viewAllGenome
import mi_viewAllGenome
import model_finder
import mrbayes
import trimal
from completeGeneToTxt import completeGeneToTxt
from download_file import download_file
from PySide6.QtGui import QIcon
from PySide6.QtWebEngineWidgets import QWebEngineView
import resources
from split_to_fasta import split_to_fasta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

fold = os.getcwd()
ch_cds = f"{fold}/chloroplast_cds"
mi_cds = f"{fold}/mitochondrial_cds"
ch_selection = []
mi_selection = []
conserved_sequence=[]
all_genes_selected = True
time1=''

class Stats(QMainWindow):
    def __init__(self):
        super().__init__()



        self.ui = QUiLoader().load('ui/brandnew.ui')
        icon = QIcon('ui/ziyuan/tubiao.png')
        self.ui.setWindowIcon(icon)


        #treeWidget
        self.ch_levels = ["kingdom", "phylum", "class", "Orderr", "family", "genus", "species"]
        self.ch_conn = sqlite3.connect('chloroplast_species_nc.db')
        self.ch_cursor = self.ch_conn.cursor()
        self.mi_levels = ["kingdom", "phylum", "class", "Orderr", "family", "genus", "species"]
        self.mi_conn = sqlite3.connect('mitochondrion_species_nc.db')
        self.mi_cursor = self.mi_conn.cursor()
        self.ui.ch_tree.itemExpanded.connect(self.ch_handleExpanded)
        self.ui.ch_tree.itemChanged.connect(self.ch_handleItemChanged)
        self.ch_fill_top_tree_widget()
        self.ui.mi_tree.itemExpanded.connect(self.mi_handleExpanded)
        self.ui.mi_tree.itemChanged.connect(self.mi_handleItemChanged)
        self.mi_fill_top_tree_widget()

        #main
        self.ui.chlo.clicked.connect(self.chlo)
        self.ui.mito.clicked.connect(self.mito)
        self.ui.mi_add.clicked.connect(self.mi_add)
        self.ui.ch_add.clicked.connect(self.ch_add)

        #geneview
        self.ui.geneview.clicked.connect(self.geneview)
        self.ui.excel.clicked.connect(self.execl)

        #alignment
        self.ui.mito_2.clicked.connect(self.mito_2)
        self.ui.mito_select.clicked.connect(self.mito_select)
        self.ui.mi_gen.clicked.connect(self.mi_gen)

        self.ui.chlo_2.clicked.connect(self.chlo_2)
        self.ui.chlo_select.clicked.connect(self.chlo_select)
        self.ui.ch_gen.clicked.connect(self.ch_gen)

        #iqtree
        self.combobox = self.ui.iqGroupSelect
        self.model = QStandardItemModel()
        self.combobox.setModel(self.model)
        self.combobox.view().viewport().installEventFilter(self)
        self.combobox.view().pressed.connect(self.handle_item_pressed)
        self.ui.iqtree.clicked.connect(self.iqtree)
        self.ui.iqtree_2.clicked.connect(self.iqtree_2)

        #modelfinder+fasttree
        self.ui.fasttree.clicked.connect(self.fasttree)
        self.ui.fasttree_2.clicked.connect(self.fasttree_2)
        self.ui.modelfinder.clicked.connect(self.modelfinder)

        #mrbayes
        self.combobox3=self.ui.mbout
        self.model3 = QStandardItemModel()
        self.combobox3.setModel(self.model3)
        self.combobox3.view().viewport().installEventFilter(self)
        self.combobox3.view().pressed.connect(self.handle_item_pressed_3)
        self.ui.bayes.clicked.connect(self.bayes)
        self.ui.mrbayes.clicked.connect(self.mrbayes)

        #PAML
        self.ui.paml.clicked.connect(self.paml)
        self.ui.paml_2.clicked.connect(self.paml_2)

        #iTOL
        self.ui.viewtree.clicked.connect(self.web)

        #Pic
        self.ui.viewtree_2.clicked.connect(self.pic)
        #Trex
        self.ui.Trex.clicked.connect(self.treefile_to_trex)
        #manage
        self.ui.pushButton.clicked.connect(self.manage)
        #about
        self.ui.pushButton_2.clicked.connect(self.about)
        self.ui.pushButton_3.clicked.connect(self.Acknowledgment)
        #github
        self.ui.github.clicked.connect(self.github)

    def github(self):
        url="https://github.com/y1273725502/POPP"
        webbrowser.open_new(url)

    def Acknowledgment(self):
        QMessageBox.about(self.ui,"Acknowledgment","Thank you Mr. Bi for your guidance")

    def about(self):
        QMessageBox.about(self.ui,"ABOUT","Written by BorisYu and licensed under GPL3.0")
    def manage(self):
        selectGene = mi_speciesManage.Stats()
        selectGene.ui.show()
    def treefile_to_trex(self):

        self.ui.tabWidget.setCurrentIndex(11)
        # # 启动浏览器并导航到iTOL的上传页面
        # options = webdriver.EdgeOptions()
        # options.add_argument('--headless')
        # driver = webdriver.Edge(options=options)  # 使用Chrome作为示例，你可能需要根据你的浏览器修改这一行
        # driver.get("http://trex.uqam.ca/index.php?action=newick&project=trex")  # iTOL的上传页面URL，确保这是正确的
        #
        with open(rf'{time1}\temp.fasta.treefile', 'r', encoding='utf-8') as file:  # 替换为你的文件名和编码
            content = file.read()
        clipboard=app.clipboard()
        clipboard.setText(content)
        # textarea_xpath = "/html/body/table/tbody/tr/td/div/div/table[2]/tbody/tr[1]/td/table/tbody/tr/td[3]/table/tbody/tr[3]/td/form/table/tbody/tr[3]/td/textarea"
        # textarea = driver.find_element(By.XPATH,textarea_xpath)
        # textarea.clear()  # 清除文本框中现有的内容（如果有的话）
        # textarea.send_keys(content)  # 发送文件内容到文本框
        #
        # submit_button=r'/html/body/table/tbody/tr/td/div/div/table[2]/tbody/tr[1]/td/table/tbody/tr/td[3]/table/tbody/tr[3]/td/form/table/tbody/tr[5]/td/input[1]'
        # submit=driver.find_element(By.XPATH,submit_button)
        # submit.click()
        # # 从Selenium中获取cookies
        # selenium_cookies = driver.get_cookies()
        view=self.ui.web2
        # profile = QWebEngineProfile.defaultProfile()
        # print(selenium_cookies)
        # # 遍历 Selenium 获取的 cookies 并设置它们
        # for selenium_cookie in selenium_cookies:
        #     # 转换 Selenium cookie 字典为 QWebEngine 可以接受的格式
        #     # 注意：QWebEngineCookieStore.setCookie() 需要一个包含特定键的字典
        #     cookie_dict = {
        #         'name': selenium_cookie['name'],
        #         'value': selenium_cookie['value']
        #         # Selenium 使用的是 Unix 时间戳（秒），需要转换为毫秒
        #         # 注意：QWebEngineCookieStore 不直接支持 secure, httpOnly, sameSite 等属性，你可能需要其他方法来处理它们
        #     }
        #     # 创建一个 QNetworkCookie 对象
        #     cookie = QNetworkCookie()
        #     cookie.setName(QByteArray(cookie_dict['name'].encode('utf-8')))  # 将字符串转换为字节数组
        #     cookie.setValue(QByteArray(cookie_dict['value'].encode('utf-8')))  # 同样转换值
        # #
        # #         # 设置 cookie
        #
        #     profile.cookieStore().setCookie(cookie)
        #     print(profile.cookieStore().loadAllCookies())
        view.load(QUrl('https://phylo.io/#'))
        QMessageBox().about(self.ui, "successful", "The tree file has been written to the clipboard!")


    def ch_add(self):
        self.ui.ch_list.clear()
        global ch_selection
        ch_selection=[]
        selected_leaf_items = self.ch_get_checked_leaf_items()
        for item in selected_leaf_items:
            ch_selection.append(item.text(0))
        self.ui.ch_list.addItem("Species that have been added")
        for i in ch_selection:
            self.ui.ch_list.addItem('\t'+i)
        print(ch_selection)
    def mi_add(self):
        self.ui.mi_list.clear()
        global mi_selection
        mi_selection=[]
        selected_leaf_items = self.mi_get_checked_leaf_items()
        for item in selected_leaf_items:
            mi_selection.append(item.text(0))
        self.ui.mi_list.addItem("Species that have been added")
        for i in mi_selection:
            self.ui.mi_list.addItem('\t'+i)
        print(mi_selection)


    def chlo(self):
        self.ui.tabWidget.setCurrentIndex(5)
    def mito(self):
        self.ui.tabWidget.setCurrentIndex(4)

    def mito_2(self):
        self.ui.tabWidget.setCurrentIndex(2)
        self.mi_download_selected_file()
        # 获取当前日期和时间
        now = datetime.datetime.now()
        # 格式化日期和时间的输出
        date_time = now.strftime("%Y-%m-%d-%H-%M-%S")
        # 创建文件夹名
        folder_name = f"{date_time}"
        global time1
        time1=folder_name
        # 检查文件夹是否已存在，如果没有则创建新文件夹
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        global time
        time=folder_name
        allSequences = findAllGene.findAllGene(mi_selection, mi_cds, 'mitochondrion_species_nc.db')
        geneToFolder.geneToFolder(allSequences, mi_selection, mi_cds, folder_name, 'mitochondrion_species_nc.db')
        global conserved_sequence
        conserved_sequence = conservedSequence.conservedSequence(mi_selection, fold + "/mitochondrial_cds",
                                                                 'mitochondrion_species_nc.db')

    def chlo_2(self):
        self.ui.tabWidget.setCurrentIndex(3)
        self.ch_download_selected_file()
        # 获取当前日期和时间
        now = datetime.datetime.now()
        # 格式化日期和时间的输出
        date_time = now.strftime("%Y-%m-%d-%H-%M-%S")
        # 创建文件夹名
        folder_name = f"{date_time}"
        global time1
        time1=folder_name
        # 检查文件夹是否已存在，如果没有则创建新文件夹
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        allSequences = findAllGene.findAllGene(ch_selection, ch_cds, 'chloroplast_species_nc.db')
        geneToFolder.geneToFolder(allSequences, ch_selection, ch_cds, folder_name, 'chloroplast_species_nc.db')
        global conserved_sequence
        conserved_sequence = conservedSequence.conservedSequence(ch_selection, fold + "/chloroplast_cds",
                                                                 'chloroplast_species_nc.db')

    def mito_select(self):
        def custom_sort(gene):
            return gene[0]

        # 对基因列表进行排序
        sorted_gene_list = sorted(conserved_sequence, key=custom_sort)
        # 打印排序后的基因列表
        print(sorted_gene_list)
        selectGene = geneSelection.Stats(sorted_gene_list, time1)
        selectGene.ui.show()

    def chlo_select(self):
        def custom_sort(gene):
            return gene[0]

        # 对基因列表进行排序
        sorted_gene_list = sorted(conserved_sequence, key=custom_sort)
        # 打印排序后的基因列表
        print(sorted_gene_list)
        selectGene = geneSelection.Stats(sorted_gene_list, time1)
        selectGene.ui.show()

    def ch_gen(self):
        selectedGene = []
        with open(f"{time1}\\list_file.txt", "r") as file:
            for line in file:
                selectedGene.append(line.strip())
        print(selectedGene)
        pairWay = self.ui.pairWay_2.currentText()
        pairWork = self.ui.pairWork.currentText()
        if pairWay == 'MAFFT':
            if pairWork == 'Conserved Sequence':
                for gene in selectedGene:
                    mafftWay.mafftWay(time1, gene)
                    trimal.trimAl(time1, gene)
                split_to_fasta(time1, ch_selection, selectedGene)
            elif pairWork == 'Complete genome':
                for item in ch_selection:
                    id = self.name_to_id(item, 'chloroplast_species_nc.db')
                    if os.path.isfile(fold + "/chloroplast_cds" + "/" + id + '_complete.txt'):
                        pass
                    else:
                        downloadCompleteGenome.download_file(id, fold + "/chloroplast_cds")
                for item in ch_selection:
                    id = self.name_to_id(item, 'chloroplast_species_nc.db')
                    if os.path.isfile(fold + "/chloroplast_cds" + "/" + id + '_complete.txt'):
                        completeGeneToTxt(fold + "/chloroplast_cds", id, time1)
                    else:
                        print("No complete genome")
                mafftWay.mafftWayAll(time1)
                trimal.trimAlAll(time1)


        elif pairWay == 'ClustalW':
            if pairWork == 'Conserved Sequence':

                for gene in selectedGene:
                    clustal.clustal(time1, gene)
                    trimal.trimAl(time1, gene)
                split_to_fasta(time1, ch_selection, selectedGene)
            elif pairWork == 'Complete genome':
                for item in ch_selection:
                    id = self.name_to_id(item, 'chloroplast_species_nc.db')
                    if os.path.isfile(fold + "/chloroplast_cds" + "/" + id + '_complete.txt'):
                        pass
                    else:
                        downloadCompleteGenome.download_file(id, fold + "/chloroplast_cds")
                for item in ch_selection:
                    id = self.name_to_id(item, 'chloroplast_species_nc.db')
                    if os.path.isfile(fold + "/chloroplast_cds" + "/" + id + '_complete.txt'):
                        completeGeneToTxt(fold + "/chloroplast_cds", id, time1)
                    else:
                        print("No complete genome")
                clustal.clustalAll(time1)
                trimal.trimAlAll(time1)


        elif pairWay == 'Muscle':
            if pairWork == 'Conserved Sequence':

                for gene in selectedGene:
                    Muscle.muscle(time1, gene)
                    trimal.trimAl(time1, gene)
                split_to_fasta(time1, ch_selection, selectedGene)
            elif pairWork == 'Complete genome':
                for item in ch_selection:
                    id = self.name_to_id(item, 'chloroplast_species_nc.db')
                    if os.path.isfile(fold + "/chloroplast_cds" + "/" + id + '_complete.txt'):
                        pass
                    else:
                        downloadCompleteGenome.download_file(id, fold + "/chloroplast_cds")
                for item in ch_selection:
                    id = self.name_to_id(item, 'chloroplast_species_nc.db')
                    if os.path.isfile(fold + "/chloroplast_cds" + "/" + id + '_complete.txt'):
                        completeGeneToTxt(fold + "/chloroplast_cds", id, time1)
                    else:
                        print("No complete genome")
                Muscle.muscleAll(time1)
                trimal.trimAlAll(time1)
        QMessageBox().about(self.ui, "The comparison was successful!", "The comparison was successful!")
        #show res
        with open(f"{time1}/temp.fasta", 'r', encoding='GBK') as file:
            file_content = file.read()
        self.ui.Res_2.setPlainText(file_content)

    def mi_gen(self):
        pairWay = self.ui.pairWay.currentText()
        selectedGene = []
        with open(f"{time1}\\list_file.txt", "r") as file:
            for line in file:
                selectedGene.append(line.strip())
        print(selectedGene)

        if pairWay == 'MAFFT':
            for gene in selectedGene:
                mafftWay.mafftWay(time1, gene)
                trimal.trimAl(time1, gene)
            split_to_fasta(time1, mi_selection, selectedGene)

        elif pairWay == 'ClustalW':
            for gene in selectedGene:
                clustal.clustal(time1, gene)
                trimal.trimAl(time1, gene)
            split_to_fasta(time1, mi_selection, selectedGene)

        elif pairWay == 'Muscle':
            for gene in selectedGene:
                Muscle.muscle(time1, gene)
                trimal.trimAl(time1, gene)
            split_to_fasta(time1, mi_selection, selectedGene)
        QMessageBox().about(self.ui, "The comparison was successful!", "The comparison was successful!")

        #show res
        with open(f"{time1}/temp.fasta", 'r', encoding='GBK') as file:
            file_content = file.read()
        self.ui.Res.setPlainText(file_content)
    def geneview(self):
        self.ui.tabWidget.setCurrentIndex(1)
        if mi_selection:
            self.mi_download_selected_file()
            allSequences = findAllGene.findAllGene(mi_selection, mi_cds, 'mitochondrion_species_nc.db')
            dict = geneForEachSpec.geneForEachSpec(mi_selection, mi_cds, 'mitochondrion_species_nc.db')

            # 定义一个自定义的排序函数，按照基因名称的第一个字母排序
            def custom_sort(gene):
                return gene[0]
            spec=mi_selection
            # 对基因列表进行排序
            allgenes = sorted(allSequences, key=custom_sort)

            conserved = conservedSequence.conservedSequence(mi_selection, mi_cds, 'mitochondrion_species_nc.db')
            self.ui.conserved.setText(f'There were {len(conserved)} conserved genes')
            table = self.ui.table
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
        else:
            self.ch_download_selected_file()
            allSequences = findAllGene.findAllGene(ch_selection, ch_cds, 'chloroplast_species_nc.db')
            dict = geneForEachSpec.geneForEachSpec(ch_selection, ch_cds, 'chloroplast_species_nc.db')

            # 定义一个自定义的排序函数，按照基因名称的第一个字母排序
            def custom_sort(gene):
                return gene[0]

            spec = ch_selection
            # 对基因列表进行排序
            allgenes = sorted(allSequences, key=custom_sort)

            conserved = conservedSequence.conservedSequence(ch_selection, ch_cds, 'chloroplast_species_nc.db')
            self.ui.conserved.setText(f'There were {len(conserved)} conserved genes')
            table = self.ui.table
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

    def iqtree(self):
        self.ui.tabWidget.setCurrentIndex(6)

        if ch_selection:
            for item_text in ch_selection:
                item = QStandardItem(item_text)
                item.setCheckable(True)
                item.setCheckState(Qt.Unchecked)
                self.model.appendRow(item)
        else:
            for item_text in mi_selection:
                item = QStandardItem(item_text)
                item.setCheckable(True)
                item.setCheckState(Qt.Unchecked)
                self.model.appendRow(item)

    def iqtree_2(self):
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
                    iqTree.tree(time1, "", f"-bb {num}", "", "-redo")
                else:
                    iqTree.tree(time1, "", f"-bb {num}", "-m", f"{modSelect} -redo")
            elif bootSelect == 'Standard':
                if modSelect == "AUTO":
                    iqTree.tree(time1, f"-b {num}", "", "", "-redo")
                else:
                    iqTree.tree(time1, f"-b {num}", "", "-m", f"{modSelect} -redo")
            elif bootSelect == 'None':
                if modSelect == "AUTO":
                    iqTree.tree(time1, "", "", "", "-redo")
                else:
                    iqTree.tree(time1, "", "", "-m", f"{modSelect} -redo")
        else:
            if bootSelect == 'Ultrafast':
                if modSelect == "AUTO":
                    iqTree.tree(time1, "", f"-bb {num}", "-o", f"{outGroup} -redo")
                else:
                    iqTree.tree(time1, "", f"-bb {num}", "-o", f"{outGroup} -m {modSelect} -redo")
            elif bootSelect == 'Standard':
                if modSelect == 'AUTO':
                    iqTree.tree(time1, f"-b {num}", "", "-o", f"{outGroup} -redo")
                else:
                    iqTree.tree(time1, f"-b {num}", "", "-o", f"{outGroup} -m {modSelect} -redo")
            elif bootSelect == 'None':
                if modSelect == "AUTO":
                    iqTree.tree(time1, "", "", "-o", f"{outGroup} -redo")
                else:
                    iqTree.tree(time1, "", "", "-o", f"{outGroup} -m {modSelect} -redo")
        QMessageBox().about(self.ui, "successful", "Generating the Evolutionary Tree successfully!")
        folder_path = f"{time1}"  # 请替换为你的文件夹路径
        os.startfile(folder_path)

    def fasttree(self):
        self.ui.tabWidget.setCurrentIndex(7)

    def fasttree_2(self):
        mods = self.ui.mods.currentText()
        if mods == "GTR":
            Fasttree.tree(time1, "-gtr -nt")
        elif mods == "JTT":
            Fasttree.tree(time1, "")
        elif mods == "LG":
            Fasttree.tree(time1, "-lg")
        elif mods == "WAG":
            Fasttree.tree(time1, "-wag")
        QMessageBox().about(self.ui, "successful", "Generating the Evolutionary Tree successfully!")
        folder_path = f"{time1}"  # 请替换为你的文件夹路径
        os.startfile(folder_path)

    def modelfinder(self):
        model_finder.tree(time1, '', '')
        # show res
        with open(f"{time1}/temp.fasta.log", 'r', encoding='GBK') as file:
            file_content = file.read()
        self.ui.model_res.setPlainText(file_content)

    def bayes(self):
        self.ui.tabWidget.setCurrentIndex(8)
        if ch_selection:
            for item_text in ch_selection:
                item = QStandardItem(item_text)
                item.setCheckable(True)
                item.setCheckState(Qt.Unchecked)
                self.model3.appendRow(item)
        else:
            for item_text in mi_selection:
                item = QStandardItem(item_text)
                item.setCheckable(True)
                item.setCheckState(Qt.Unchecked)
                self.model3.appendRow(item)

    def mrbayes(self):
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
        numChains = self.ui.numChains.text()
        mrbayes.tree(time1, outgroup, gnum, SampFreq, printFreq, numChains)
        QMessageBox().about(self.ui, "successful", "Generating the Evolutionary Tree successfully!")
        folder_path = f"{time1}"  # 请替换为你的文件夹路径
        os.startfile(folder_path)

    def paml(self):
        self.ui.tabWidget.setCurrentIndex(9)

    def paml_2(self):
        seq = self.ui.seq.text()
        noisy = self.ui.noisy.text()
        rate = self.ui.rate.text()
        model = self.ui.model.text()
        ns = self.ui.ns.text()
        codon = self.ui.codon.text()
        clean = self.ui.clean.text()
        fix = self.ui.fix.text()
        kappa = self.ui.kappa.text()
        try:
            PAML.run_paml(f"{time1}/temp.fasta", f"{time1}/temp.fasta.treefile", f"{time1}/output_file", seq, noisy, rate,
                          model, ns, codon, clean, fix, kappa)
        except:
            print("OK")
        # 读取文件内容
        with open(f"{time1}/output_file", 'r', encoding='GBK') as file:
            file_content = file.read()
        # 将内容显示到QPlainTextEdit中
        self.ui.paml_res.setPlainText(file_content)

    def web(self):
        self.ui.tabWidget.setCurrentIndex(10)
        self.treefile_to_itol()

    def treefile_to_itol(self):
        # # 启动浏览器并导航到iTOL的上传页面
        # options = webdriver.EdgeOptions()
        # options.add_argument('--headless')
        # driver = webdriver.Edge(options=options)  # 使用Chrome作为示例，你可能需要根据你的浏览器修改这一行
        # driver.get("https://itol.embl.de/upload.cgi")  # iTOL的上传页面URL，确保这是正确的
        #
        # # 等待文件上传输入元素出现（如果有需要的话）
        # file_input = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div/div[2]/form/div[3]/input'))  # 使用实际的ID或其他选择器
        # )
        #
        # file_path = r"C:\Users\12737\Documents\Capstone_project\temp.fasta.treefile"
        # file_input.send_keys(file_path)
        #
        # submit_button = driver.find_element(By.XPATH,r'/html/body/div[1]/div/div[2]/form/p[2]')  # 使用实际的ID或其他选择器
        # submit_button.location_once_scrolled_into_view
        # submit_button.click()
        #
        # wait = WebDriverWait(driver, 60)  # 等待最多60秒
        # element = wait.until(EC.visibility_of_element_located((By.XPATH, r'/html/body/div[14]/div[1]/div[1]/div[2]/div')))
        #
        # # 获取当前页面的URL，这应该是上传完成后的页面
        # current_url = driver.current_url
        # print("上传完成后的页面URL:", current_url)

        with open(rf'{time1}\temp.fasta.treefile', 'r', encoding='utf-8') as file:  # 替换为你的文件名和编码
            content = file.read()
        clipboard=app.clipboard()
        clipboard.setText(content)

        self.ui.web1.load("https://itol.embl.de/upload.cgi")
        QMessageBox().about(self.ui, "successful", "The tree file has been written to the clipboard!")

    def pic(self):
        self.ui.tabWidget.setCurrentIndex(12)
        self.scene = QGraphicsScene()
        self.ui.treePic.setScene(self.scene)
        self.load_image(f"{time1}/tree.png")

    def load_image(self, filename):
        # 加载图像文件
        pixmap = QPixmap(filename)
        # 清空场景
        self.scene.clear()
        # 创建图像项目
        pixmap_item = self.scene.addPixmap(pixmap)
        # 获取视图大小
        view_rect = self.ui.treePic.viewport().rect()

        # 设置图像在视图中居中显示
        pixmap_item.setPos((view_rect.width() - pixmap.width()) / 2,
                           (view_rect.height() - pixmap.height()) / 2)

        # 设置图像填充整个视图
        self.scene.setSceneRect(0, 0, view_rect.width(), view_rect.height())

    def handle_item_pressed(self, index):
        item = self.model.itemFromIndex(index)
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)

    def handle_item_pressed_3(self, index):
        item = self.model3.itemFromIndex(index)
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)

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
    def name_to_id(self, item, database):
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
app = QApplication([])
stats = Stats()

stats.ui.show()
app.exec()
