import os

import matplotlib
import numpy as np
from Bio import Phylo
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QGraphicsScene, QApplication, QLabel, QMessageBox
from matplotlib import pyplot as plt

color=0
class Stats:
    def __init__(self,time):
        super().__init__()
        self.ui = QUiLoader().load('ui/tree.ui')
        self.setRotatedLabel('Tree editing')
        # 创建 QTimer 对象，设置长按时间为1000ms
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.on_long_press)

        self.scene = QGraphicsScene()
        self.ui.treePic.setScene(self.scene)
        self.load_image(f"{time}/tree.png")
        self.ui.flash.clicked.connect(lambda:self.flash(time))
        self.ui.modify.clicked.connect(lambda:self.modify(time))

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

    def modify(self,time):
        old = self.ui.old.text()
        new = self.ui.new1.text()

        with open(f"{time}/temp.fasta.treefile", 'r') as file:
            data = file.read()

        data = data.replace(f"{old}",f"{new}")
        with open(f"{time}/temp.fasta.treefile", 'w') as file:
            file.write(data)

        tree = Phylo.read(f"{time}/temp.fasta.treefile", "newick")
        Phylo.draw(tree, do_show=False)
        # 删除原来的png文件
        if os.path.exists(f"{time}/tree.png"):
            os.remove(f"{time}/tree.png")
        plt.savefig(f"{time}/tree.png")
        QMessageBox().about(self.ui, "The name was modified!", "The name was modified!")


    def get_species(self,tree):
        # 提取物种名称
        names = [leaf.name.split("_")[0] for leaf in tree.get_terminals()]
        # 使用set去除重复的名称
        return set(names)

    def ancestor(self,ances,time):
        # 读取treefile文件
        tree = Phylo.read(f"{time}/temp.fasta.treefile", "newick")

        mrca = tree.common_ancestor({'name': ances})
        # 使用root_with_outgroup方法进行重新设置根节点
        tree.root_with_outgroup(mrca)
        Phylo.draw(tree,do_show=False)
        # 删除原来的png文件
        if os.path.exists(f"{time}/tree.png"):
            os.remove(f"{time}/tree.png")
        plt.savefig(f"{time}/tree.png")
        QMessageBox().about(self.ui, "success!", f"Successfully set {ances} to ancestor!")

    def color(self,time):
        # 读取treefile文件
        tree = Phylo.read(f"{time}/temp.fasta.treefile", "newick")

        # 获取所有不同的物种
        species = self.get_species(tree)

        # 设置颜色
        colors = plt.cm.rainbow(np.linspace(0, 1, len(species)))

        # 转换为十六进制RGB颜色代码
        colors = [matplotlib.colors.to_hex(c) for c in colors]

        species_color = dict(zip(species, colors))
        # 调用函数为每一个物种变色
        self.color_species(tree,species_color)

        Phylo.draw(tree,do_show=False)
        # 删除原来的png文件
        if os.path.exists(f"{time}/tree.png"):
            os.remove(f"{time}/tree.png")
        plt.savefig(f"{time}/tree.png")

    def color_n_ancestor(self,ances,time):
        # 读取treefile文件
        tree = Phylo.read(f"{time}/temp.fasta.treefile", "newick")

        mrca = tree.common_ancestor({'name': ances})
        # 使用root_with_outgroup方法进行重新设置根节点
        tree.root_with_outgroup(mrca)
        # 获取所有不同的物种
        species = self.get_species(tree)

        # 设置颜色
        colors = plt.cm.rainbow(np.linspace(0, 1, len(species)))

        # 转换为十六进制RGB颜色代码
        colors = [matplotlib.colors.to_hex(c) for c in colors]

        species_color = dict(zip(species, colors))
        # 调用函数为每一个物种变色
        self.color_species(tree,species_color)

        Phylo.draw(tree,do_show=False)
        # 删除原来的png文件
        if os.path.exists(f"{time}/tree.png"):
            os.remove(f"{time}/tree.png")
        plt.savefig(f"{time}/tree.png")
        QMessageBox().about(self.ui, "success!", "Successfully colored!")


    def flash(self,time):
        text = self.ui.rootTxt.text()
        if not text.strip():
            self.load_image(f"{time}/tree.png")
        else:
            ances=text
            self.ancestor(ances,time)
            self.load_image(f"{time}/tree.png")



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

    def color_species(self,tree,species_color):
        for clade in tree.find_clades():
            if clade.name:
                species = clade.name.split("_")[0]
                clade.color = species_color[species]
