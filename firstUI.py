from PySide6.QtGui import QPixmap
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
import chloroplastUI
import mitochondrialUI


class Stats:
    def __init__(self):
        super().__init__()
        self.ui = QUiLoader().load('ui/firstUI.ui')

        # 创建两个 QGraphicsView
        self.ch_view = self.ui.ch
        self.mi_view = self.ui.mi

        # 创建两个 QGraphicsScene
        self.scene_ch = QGraphicsScene()
        self.scene_mi = QGraphicsScene()

        # 分别加载不同的图片到场景中
        pixmap_ch = QPixmap("chloroplast.jpg")
        pixmap_mi = QPixmap("mitochondria.jpg")

        self.scene_ch.addPixmap(pixmap_ch)
        self.scene_mi.addPixmap(pixmap_mi)

        # 设置场景
        self.ch_view.setScene(self.scene_ch)
        self.mi_view.setScene(self.scene_mi)

        self.ui.chButton.clicked.connect(self.chUI)
        self.ui.miButton.clicked.connect(self.miUI)

    def chUI(self):
        self.chlo = chloroplastUI.Stats()
        self.chlo.ui.show()

    def miUI(self):
        self.mito = mitochondrialUI.Stats()
        self.mito.ui.show()

app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec_()
