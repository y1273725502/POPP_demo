import os
import sqlite3

from PySide6.QtCore import QTimer, Qt, Slot
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QLabel, QTableWidgetItem, QDialog, QMessageBox

import Muscle
import clustal
import conservedSequence
import downloadCompleteGenome
import geneSelection
import mafftWay
import seeAlignRes
import toTreeUI
import trimal
from completeGeneToTxt import completeGeneToTxt
from split_to_fasta import split_to_fasta

class Stats:
    def __init__(self, time, seletion, fold):

        super().__init__()
        self.ui = QUiLoader().load('ui/ch_tree.ui')
        self.setRotatedLabel('Generate tree')
        self.ui.seeAlignRes.clicked.connect(lambda: self.seeAlignRes(time))
        self.ui.pairRes.clicked.connect(lambda: self.pairRes(time, seletion, fold + "/chloroplast_cds"))
        self.ui.editTree.clicked.connect(lambda: self.toTree(time, seletion))
        conserved_sequence = conservedSequence.conservedSequence(seletion, fold + "/chloroplast_cds",
                                                                 'chloroplast_species_nc.db')

        self.ui.select.clicked.connect(lambda: self.geneSelection(conserved_sequence,time))


    def toTree(self, time, selection):
        self.toTreee = toTreeUI.Stats(time, selection)
        self.toTreee.ui.show()

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

    def geneSelection(self, conserved_sequence, date_time):
        # 定义一个自定义的排序函数，按照基因名称的第一个字母排序
        def custom_sort(gene):
            return gene[0]

        # 对基因列表进行排序
        sorted_gene_list = sorted(conserved_sequence, key=custom_sort)
        # 打印排序后的基因列表
        print(sorted_gene_list)
        selectGene = geneSelection.Stats(sorted_gene_list, date_time)
        selectGene.ui.show()

    def pairRes(self, date_time, selection, work_fold):
        selectedGene = []
        with open(f"{date_time}\\list_file.txt", "r") as file:
            for line in file:
                selectedGene.append(line.strip())
        print(selectedGene)
        pairWay = self.ui.pairWay.currentText()
        pairWork = self.ui.pairWork.currentText()
        if pairWay == 'MAFFT':
            if pairWork == 'Conserved Sequence':
                for gene in selectedGene:
                    mafftWay.mafftWay(date_time, gene)
                    trimal.trimAl(date_time, gene)
                split_to_fasta(date_time, selection, selectedGene)
            elif pairWork == 'Complete genome':
                for item in selection:
                    id = self.name_to_id(item, 'chloroplast_species_nc.db')
                    if os.path.isfile(work_fold + "/" + id + '_complete.txt'):
                        pass
                    else:
                        downloadCompleteGenome.download_file(id, work_fold)
                for item in selection:
                    id = self.name_to_id(item, 'chloroplast_species_nc.db')
                    if os.path.isfile(work_fold + "/" + id + '_complete.txt'):
                        completeGeneToTxt(work_fold, id, date_time)
                    else:
                        print("No complete genome")
                mafftWay.mafftWayAll(date_time)
                trimal.trimAlAll(date_time)


        elif pairWay == 'ClustalW':
            if pairWork == 'Conserved Sequence':

                for gene in selectedGene:
                    clustal.clustal(date_time, gene)
                    trimal.trimAl(date_time, gene)
                split_to_fasta(date_time, selection, selectedGene)
            elif pairWork == 'Complete genome':
                for item in selection:
                    id = self.name_to_id(item, 'chloroplast_species_nc.db')
                    if os.path.isfile(work_fold + "/" + id + '_complete.txt'):
                        pass
                    else:
                        downloadCompleteGenome.download_file(id, work_fold)
                for item in selection:
                    id = self.name_to_id(item, 'chloroplast_species_nc.db')
                    if os.path.isfile(work_fold + "/" + id + '_complete.txt'):
                        completeGeneToTxt(work_fold, id, date_time)
                    else:
                        print("No complete genome")
                clustal.clustalAll(date_time)
                trimal.trimAlAll(date_time)


        elif pairWay == 'Muscle':
            if pairWork == 'Conserved Sequence':

                for gene in selectedGene:
                    Muscle.muscle(date_time, gene)
                    trimal.trimAl(date_time, gene)
                split_to_fasta(date_time, selection, selectedGene)
            elif pairWork == 'Complete genome':
                for item in selection:
                    id = self.name_to_id(item, 'chloroplast_species_nc.db')
                    if os.path.isfile(work_fold + "/" + id + '_complete.txt'):
                        pass
                    else:
                        downloadCompleteGenome.download_file(id, work_fold)
                for item in selection:
                    id = self.name_to_id(item, 'chloroplast_species_nc.db')
                    if os.path.isfile(work_fold + "/" + id + '_complete.txt'):
                        completeGeneToTxt(work_fold, id, date_time)
                    else:
                        print("No complete genome")
                Muscle.muscleAll(date_time)
                trimal.trimAlAll(date_time)
        QMessageBox().about(self.ui, "The comparison was successful!", "The comparison was successful!")

    def seeAlignRes(self, time):
        self.seealignRes = seeAlignRes.Stats(time)
        self.seealignRes.ui.show()

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
