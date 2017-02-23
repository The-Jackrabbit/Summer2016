import sys, re, string
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from palette_functions import *
from palette_config import *
from list_functions import *

bg = [128, 90, 0]


class TextBox(QLineEdit):
    def __init__(self, parent=None):
        super(TextBox, self).__init__(parent)
        pal = QPalette()
        bgc = QColor(255, 255, 255)
        pal.setColor(QPalette.Base, bgc)
        textc = QColor(0, 0, 0)
        pal.setColor(QPalette.Text, textc)
        self.setPalette(pal)


class Example(QWidget):
    global bg
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global bg

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(background[0], background[1], background[2]))
        self.setPalette(palette)

        self.col = QColor(background[0], background[1], background[2])
        print(self.col.red())
        self.red = QSlider(Qt.Horizontal, self)
        self.green = QSlider(Qt.Horizontal, self)
        self.blue = QSlider(Qt.Horizontal, self)
        self.red_box = TextBox(self)
        self.green_box = TextBox(self)
        self.blue_box = TextBox(self)

        self.sliders = [self.red, self.green, self.blue]
        self.boxes = [self.red_box, self.green_box, self.blue_box]

        for i in range(len(self.sliders)):
            self.sliders[i].setMinimum(0), self.sliders[i].setMaximum(255)
            self.sliders[i].setFocusPolicy(Qt.NoFocus)
            self.sliders[i].setGeometry(30, 30 + 30 * i, 255, 30)
            self.sliders[i].setValue(background[i])
            self.sliders[i].valueChanged[int].connect(self.changeValue)

        for j in range(len(self.boxes)):
            self.boxes[j].setText("{}".format(background[j]))
            self.boxes[j].setGeometry(300, 30 + 30 * j, 40, 20)
            self.boxes[j].textChanged[str].connect(self.swag)

        self.square = QFrame(self)
        self.square.setFrameStyle(2)
        self.square.setGeometry(350, 20, 100, 100)
        self.square.setStyleSheet("QWidget { background-color: %s }" % self.col.name())

        self.hex_box = TextBox(self)
        self.hex_box.setText(str(rgb_to_hex(background)))
        self.hex_box.setGeometry(280, 120, 60, 20)
        self.go = QPushButton("Go", self)
        self.go.setGeometry(240, 120, 30, 20)
        self.hex_box.returnPressed.connect(self.set_hex)
        self.go.clicked[bool].connect(self.set_hex)

        self.store_button = QPushButton("Store", self)
        self.store_button.setGeometry(375, 130, 50, 20)
        self.store_button.clicked[bool].connect(self.store_background)

        self.default_setting_button = QPushButton("Default", self)
        self.default_setting_button.clicked[bool].connect(self.restore_default)
        self.default_setting_button.setGeometry(10, 140, 100, 20)

        self.setGeometry(300, 300, 500, 170)
        self.setWindowTitle('Toggle button')
        self.show()

    def restore_default(self):
        default_color = [253, 239, 230]
        hexi = rgb_to_hex(default_color)
        self.hex_box.setText(hexi)
        for i in range(len(self.sliders)):
            self.boxes[i].setText(str(default_color[i]))
        self.square.setStyleSheet("QFrame { background-color: %s }" % self.col.name())

    def set_hex(self):
        source = self.sender()
        hexi = source.text()
        hexi = hexi.strip("#")
        hex_list = remove_trash(list(hexi), base_sixteen)
        hexi = "".join(hex_list)
        print(hexi)
        if len(list(hexi)) < 6:
            while len(list(hexi)) < 6:
                hexi += "0"
        rgb = hex_to_rgb(hexi)
        self.hex_box.setText(hexi)
        for i in range(len(self.sliders)):
            if i == 0:  self.col.setRed(rgb[0])
            if i == 1: self.col.setGreen(rgb[1])
            if i == 2: self.col.setBlue(rgb[2])
            self.boxes[i].setText(str(rgb[i]))
        self.square.setStyleSheet("QFrame { background-color: %s }" % self.col.name())

    def changeValue(self, value):
        source = self.sender()
        for i in range(len(self.sliders)):
            if source is self.sliders[i]:
                if i == 0:  self.col.setRed(value)
                if i == 1: self.col.setGreen(value)
                if i == 2: self.col.setBlue(value)
                self.boxes[i].setText(str(value))
        self.hex_box.setText(str(rgb_to_hex([self.col.red(), self.col.green(), self.col.blue()])))
        self.square.setStyleSheet("QFrame { background-color: %s }" % self.col.name())

    def swag(self):
        source = self.sender()
        v = source.text()
        check = 0
        alphabet = list(string.ascii_letters)
        if v is not "":
            for letter in alphabet:
                if letter in v:
                    check = 1
            if check == 0:
                for i in range(len(self.boxes)):
                    if source is self.boxes[i]:
                        self.sliders[i].setValue(int(v))

    def store_background(self):
        global bg
        bg = [self.col.red(), self.col.green(), self.col.blue()]
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(bg[0], bg[1], bg[2]))
        self.setPalette(palette)
        file = open("C:\\Users\Luke\PycharmProjects\Summer\\palette_config_text.txt", "w")
        file.write('bg = [{}'.format(str(bg[0])) + ', {}'.format(str(bg[1])) + ', {}'.format(str(bg[2]) + ']'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())