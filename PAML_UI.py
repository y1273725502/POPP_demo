import os

from PySide6.QtCore import Qt, QEvent, QTimer
from PySide6.QtGui import QStandardItemModel, QStandardItem, QPixmap, QPainter, QColor, QFont
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QComboBox, QMainWindow, QApplication, QLabel, QMessageBox

import Fasttree
import PAML
import PAML_Res
import finderRes
import iqTree
import model_finder
import mrbayes
import treeUI
class Stats(QMainWindow):
    def __init__(self,time,select):
        super().__init__()
        self.ui = QUiLoader().load('ui/PAML.ui')
        self.setRotatedLabel('PAML')
        self.ui.generate.clicked.connect(lambda:self.PAML(time))
        self.ui.log.clicked.connect(lambda:self.seeLog(time))
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
    def PAML(self,time):
        seq=self.ui.seq.text()
        noisy=self.ui.noisy.text()
        rate=self.ui.rate.text()
        model = self.ui.model.text()
        ns = self.ui.ns.text()
        codon = self.ui.codon.text()
        clean = self.ui.clean.text()
        fix = self.ui.fix.text()
        kappa = self.ui.kappa.text()
        PAML.run_paml(f"{time}/temp.fasta",f"{time}/temp.fasta.treefile",f"{time}/output_file",seq,noisy,rate,model,ns,codon,clean,fix,kappa)
        QMessageBox().about(self.ui, "successful", "Generate maximum likelihood results successfully!")
    def seeLog(self,time):
        self.seeRes = PAML_Res.Stats(time)
        self.seeRes.ui.show()