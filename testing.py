import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return list(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.btn = QPushButton('Dialog', self)
        self.btn.move(300, 650)
        self.btn.clicked.connect(self.showDialog)
        self.setGeometry(100, 100, 1300, 700)  # x, y, length, height
        self.setWindowTitle('Palette')
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(0, 0, 900, 40)
        self.pbar.move(200, 650)
        self.timer = QBasicTimer()
        self.step = 0

        self.setWindowTitle('QProgressBar')
        self.show()

    def paintEvent(self, e):

        qp = QPainter()
        qp.begin(self)
        self.draw_rectangles(qp)
        # self.draw_album(qp)

        qp.end()

    def draw_rectangles(self, qp):

        qp.setBrush(QColor(208, 243, 216))
        qp.drawRect(0, 0, 3840, 2160)
        qp.setBrush(QColor(255, 255, 255))
        qp.drawRect(100, 100, 500, 500)
        qp.setBrush(QColor(255, 255, 255))
        qp.drawRect(700, 100, 500, 500)

    def draw_album(self, qp):
        image = QImage('ys.gif')
        qp.begin(image)
        qp.drawImage(100, 100, image)
        qp.end()

    def showDialog(self):

        text, ok = QInputDialog.getText(self, 'Input Dialog',
            'Enter your name:')

        if ok:
            self.le.setText(str(text))


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())