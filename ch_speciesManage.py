import os
import shutil
import sqlite3

from PySide6 import QtCore
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont, QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QLabel, QFileDialog, QApplication, QMessageBox

import chloroplast_tax
import filter_chloroplast
import filter_mitochondrial
import get_chloroplast_nuccore_result
import get_mitochondria_nuccore_result
import mitochondrial_tax

fold=os.getcwd()

class Stats:
    def __init__(self):
        super().__init__()
        self.ui = QUiLoader().load('ui/speciesManage.ui')
        self.ui.updatee.clicked.connect(self.updateAll)
        self.ui.add.clicked.connect(self.ch_upload)
        icon = QIcon("059_添加.png")
        self.bu = self.ui.add
        self.bu.setIcon(icon)
        self.bu.setIconSize(QtCore.QSize(32, 32))

        icon = QIcon("059_记录.png")
        self.bu = self.ui.updatee
        self.bu.setIcon(icon)
        self.bu.setIconSize(QtCore.QSize(32, 32))
        self.setRotatedLabel('Species management')
    def ch_upload(self):
        name=self.ui.uploadName.text()
        id=self.ui.uploadID.text()
        # 创建一个数据库连接
        conn = sqlite3.connect('chloroplast_species_nc.db')
        # 创建一个游标对象
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO Species VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)",
                  (name, id, "upload", "upload", "upload", "upload", "upload", "upload",name))
        # 提交更改并关闭连接
        conn.commit()
        conn.close()
        QMessageBox().about(self.ui, "Upload successfully!", "Upload successfully! Please upload program!")
        print("导入成功！请重启应用")

    def ch_pair(self):
        # 连接到SQLite数据库
        conn = sqlite3.connect('chloroplast_species_nc.db')
        cursor = conn.cursor()
        # 执行查询语句，获取"nc"列和"species"列的全部行
        query = "SELECT * FROM SpeciesNC"
        cursor.execute(query)
        # 获取查询结果
        rows = cursor.fetchall()
        conn = sqlite3.connect('chloroplast_species_nc.db')
        cursor = conn.cursor()
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Species (
                        name TEXT,
                        NCID TEXT,
                        kingdom TEXT,
                        phylum TEXT,
                        class TEXT,
                        Orderr TEXT,
                        family TEXT,
                        genus TEXT,
                        species TEXT
                    )
                """)
        for species in rows:
            # 执行查询
            cursor.execute(f'SELECT COUNT(*) FROM Species WHERE NCID="{species[1]}"')
            # 获取查询结果
            result = cursor.fetchone()
            # 检查结果
            if result[0] > 0:
                print("字符串在数据库中存在，跳过。")
            else:
                print("字符串在数据库中不存在。")
                print(species[0],species[1])
                chloroplast_tax.taxInfo(species[0],species[1])
        # 关闭连接
        conn.close()
    def mi_pair(self):
        # 连接到SQLite数据库
        conn = sqlite3.connect('mitochondrion_species_nc.db')
        cursor = conn.cursor()
        # 执行查询语句，获取"nc"列和"species"列的全部行
        query = "SELECT * FROM SpeciesNC"
        cursor.execute(query)
        # 获取查询结果
        rows = cursor.fetchall()
        conn = sqlite3.connect('mitochondrion_species_nc.db')
        cursor = conn.cursor()
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Species (
                        name TEXT,
                        NCID TEXT,
                        kingdom TEXT,
                        phylum TEXT,
                        class TEXT,
                        Orderr TEXT,
                        family TEXT,
                        genus TEXT,
                        species TEXT
                    )
                """)

        for species in rows:
            # 执行查询
            cursor.execute(f'SELECT COUNT(*) FROM Species WHERE NCID="{species[1]}"')
            # 获取查询结果
            result = cursor.fetchone()
            # 检查结果
            if result[0] > 0:
                print("字符串在数据库中存在，跳过。")
            else:
                print("字符串在数据库中不存在。")
                print(species[0],species[1])
                mitochondrial_tax.taxInfo(species[0],species[1])

        # 关闭连接
        conn.close()

    def updateAll(self):
        get_chloroplast_nuccore_result.get_chloroplast_nuccore_result(fold)
        print('downloaded')
        filter_chloroplast.filter_chloroplast(os.path.join(fold, 'chloroplast_nuccore_result.txt'))
        self.ch_pair()
        get_mitochondria_nuccore_result.get_mitochondria_nuccore_result(fold)
        print('downloaded')
        filter_mitochondrial.filter_mitochondrial(os.path.join(fold, 'mitochondria_nuccore_result.txt'))
        self.mi_pair()
        QMessageBox().about(self.ui,"Update successfully!","Update successfully!")


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
