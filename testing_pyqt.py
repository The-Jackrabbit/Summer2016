import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import re


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return list(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initialize_ui()

    def initialize_ui(self):

        button = QPushButton("Go", self)

        button.clicked.connect(self.button_one_action)
        button.resize(40, 25)
        button.move(230, 87)
        self.entry = QLineEdit(self)
        self.output = QLineEdit(self)

        self.entry.move(75, 87)
        self.output.move(300, 87)
        self.setGeometry(300, 300, 500, 200)
        self.setWindowTitle('Quit button')
        self.show()
#b7f0f3
    def draw_bg(self, rgb_list):
        qp = QPainter()
        qp.begin(self)
        print('begin')
        print(int(rgb_list[2]))
        qp.setBrush(QColor(int(rgb_list[0]), int(rgb_list[1]), int(rgb_list[2])))
        qp.drawRect(0, 0, 3840, 2160)
        qp.end()
        print('begin 2')

    def button_one_action(self):
        print(self.entry.text())
        if self.entry.text() != '':
            if sorted(self.entry.text())[0] == '#':
                rgb_list = hex_to_rgb(self.entry.text())
                self.output.setText(str(rgb_list))
                c = QColor(int(rgb_list[0]), int(rgb_list[1]), int(rgb_list[2]))
                palette = QPalette()
                palette.setColor(QPalette.Background, c)
                self.setPalette(palette)





if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())