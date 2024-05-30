from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QLabel


class Stats:
    def __init__(self,time):
        super().__init__()
        self.ui = QUiLoader().load('ui/alignRes.ui')
        self.showAlignRes(time)
        self.ui.Ok.clicked.connect(self.returnMain)
        self.setRotatedLabel('Alignment results')
        # 创建 QTimer 对象，设置长按时间为1000ms
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.on_long_press)
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
    def on_long_press(self):
        self.timer.stop()  # 停止计时器
        print("Button has been long pressed")
        self.ui.showMinimized()  # 长按后最小化窗口

    def returnMain(self):
        self.ui.close()

    def showAlignRes(self,time):

        # 读取文件内容
        with open(f"{time}/temp.fasta", 'r', encoding='GBK') as file:
            file_content = file.read()
        # 将内容显示到QPlainTextEdit中
        self.ui.Res.setPlainText(file_content)