import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import re, random

l = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
dth = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',']
r = []

x = 500
y = 200
desc = 222, 222, 255


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return list(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def dec_to_hex(rgb):
    hexidecimal = '#'
    for color in rgb:
        for a in range(len(l)):
            for b in range(len(l)):
                if color == 16*a + b:
                    hexidecimal += "{}".format(l[a]) + "{}".format(l[b])
    return hexidecimal


class PicButton(QAbstractButton):
    def __init__(self, pixmap, pixmap_pressed, pixmap_hover, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap
        self.pixmap_hover = pixmap_hover
        self.pixmap_pressed = pixmap_pressed
        self.pressed.connect(self.update)
        self.released.connect(self.update)

    def paintEvent(self, event):
        pix = self.pixmap_hover if self.underMouse() else self.pixmap
        if self.isDown():
            pix = self.pixmap_pressed
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), pix)

    def enterEvent(self, event):
        self.update()

    def leaveEvent(self, event):
        self.update()


class TextBox(QLineEdit):
    def __init__(self, parent=None):
        super(TextBox, self).__init__(parent)
        pal = QPalette()
        bgc = QColor(252, 252, 255)
        pal.setColor(QPalette.Base, bgc)
        textc = QColor(0, 0, 0)
        pal.setColor(QPalette.Text, textc)
        self.setPalette(pal)


class Example(QWidget):
    global x, y, l, r, dth

    def __init__(self):
        super().__init__()
        self.initialize_ui()

    def initialize_ui(self):
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(245, 238, 253))
        self.setPalette(palette)

        self.desc_frame = QFrame(self)
        self.col_one = QColor(252, 252, 255)
        self.desc_frame.setGeometry(50, 50, 210, 210)
        self.desc_frame.setStyleSheet("QWidget { background-color: %s }" %
        self.col_one.name())

        button = PicButton(QPixmap('button_off.png'), QPixmap('button_hover.png'), QPixmap('button_on.png'), self)
        button.clicked.connect(self.button_one_action)
        button.frameGeometry()
        button.resize(210, 210)
        button.move(50, 50)

        self.cover = QLabel(self)
        self.cover.setGeometry(60, 60, 190, 190)
        self.cover.setFont(QFont('Franklin Gothic Medium', 50))

        self.title = QLabel(self)
        self.title.setText('Hex to RGB')
        self.title.setFont(QFont('Franklin Gothic Medium', 12))
        self.title.move(58, 60)

        self.entry = TextBox(self)
        self.entry.setText('#')
        self.entry.setFrame(False)
        self.entry.setFont(QFont('Franklin Gothic Medium', 11))

        self.entry.resize(180, 32)
        self.entry.move(58, 100)
        self.entry.returnPressed.connect(self.button_one_action)

        self.output = TextBox(self)
        self.output.setFrame(False)
        self.output.setFont(QFont('Franklin Gothic Medium', 10))
        self.output.resize(180, 32)
        self.output.move(58, 125)

        self.col = QColor(0, 0, 0)
        self.square = QFrame(self)
        self.square.setGeometry(325, 25, 290, 300)
        self.square.setStyleSheet("QWidget { background-color: %s }" %
        self.col.name())

        pixmap = QPixmap("frame_small.png")
        lbl = QLabel(self)
        lbl.setPixmap(pixmap)
        lbl.move(324, 24)
        self.setGeometry(300, 300, 640, 340)
        self.setWindowTitle('Hex to RGB')
        self.setWindowIcon(QIcon('palette_build_icon_full.png'))
        self.show()

    def button_one_action(self, pressed=None):
        global l, dth
        if self.entry.text().strip('#') == '':
            ra = '#'
            for i in range(6):
                ra += random.choice(l)
            self.entry.setText('')
            self.entry.setText(ra)
        if sorted(self.entry.text())[0] == '#':
            rgb_list = hex_to_rgb(self.entry.text())
            self.output.setText(str(rgb_list))
            self.col.setRgb(int(rgb_list[0]), int(rgb_list[1]), int(rgb_list[2]))
            self.square.setStyleSheet("QFrame { background-color: %s }" % self.col.name())
        if "," in self.entry.text():
            split_phrase = list(self.entry.text())
            a = 0
            while a < len(split_phrase):
                if split_phrase[a] not in dth:
                    del(split_phrase[a])
                else:
                    a += 1
            lala = "".join(split_phrase).split(",")
            for i in range(len(lala)):
                lala[i] = int(lala[i])
            hexidecimal = dec_to_hex(lala)
            self.output.setText(str(hexidecimal))
            self.col.setRgb(int(lala[0]), int(lala[1]), int(lala[2]))
            self.square.setStyleSheet("QFrame { background-color: %s }" % self.col.name())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
