
import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout,
    QPushButton, QApplication)
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os, sys
from palette_functions import rgb_to_hex, last_fm_album_pull, art_pull, reduce_to, picture_palette, nearest_square, palette_build, resize_image
from cImage import *
master_list = []
color_profile = [6588, 77, 38, 41, '#4d2629', 613, 138, 60, 60]
photo_res = [300, 300]
'''
        [6588, 77, 38, 41, '#4d2629', 613, 138, 60, 60] tl
        [1573, 37, 56, 37, '#253825', 853, 138, 60, 60] tr
        [165, 152, 161, 170, '#98a1aa', 613, 378, 60, 60] bl
        [21, 140, 67, 96, '#8c4360', 853, 378, 60, 60] br
'''

resolution = [1050, 575]
class TextBox(QLineEdit):
    def __init__(self, parent=None):
        super(TextBox, self).__init__(parent)
        pal = QPalette()
        bgc = QColor(255, 255, 255)
        pal.setColor(QPalette.Base, bgc)
        textc = QColor(0, 0, 0)
        pal.setColor(QPalette.Text, textc)
        self.setPalette(pal)


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

'''
class Example(QWidget):
    global master_list
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(0, 200, 200))
        self.setPalette(palette)

        self.size_squared = QPushButton("9", self)
        self.size_squared.move(4000, 0)

        self.master_button = QPushButton("Draw", self)
        self.master_button.setGeometry(320, 50, 60, 40), self.master_button.clicked.connect(self.test_mutate)

        self.config_button = QPushButton("Change", self)
        self.config_button.setGeometry(320, 100, 60, 40), self.config_button.clicked.connect(self.test_change)

        self.setGeometry(300, 300, 400, 400)
        self.show()

    def swag(self, pressed):
        source = self.sender()
        print(source.text())

    def test_change(self, pressed=None):
        self.size_squared.setText("25")

    def test_mutate(self, pressed=None):
        l = [[6588, 77, 38, 41, '#4d2629'], [2969, 23, 22, 17, '#171611'], [1875, 109, 77, 64, '#6d4d40'], [1644, 175, 143, 130, '#af8f82'], [1573, 37, 56, 37, '#253825'], [1330, 143, 111, 96, '#8f6f60'], [1182, 197, 194, 213, '#c5c2d5'], [1070, 186, 181, 159, '#bab59f'], [813, 154, 157, 202, '#9a9dca'], [380, 77, 80, 99, '#4d5063'], [373, 132, 38, 36, '#842624'], [318, 68, 86, 62, '#44563e'], [312, 115, 122, 138, '#737a8a'], [282, 229, 216, 226, '#e5d8e2'], [270, 117, 123, 175, '#757baf'], [269, 94, 76, 28, '#5e4c1c'], [225, 218, 191, 170, '#dabfaa'], [210, 112, 130, 108, '#70826c'], [200, 195, 182, 129, '#c3b681'], [185, 96, 117, 74, '#60754a'], [165, 152, 161, 170, '#98a1aa'], [61, 161, 148, 95, '#a1945f'], [55, 147, 132, 39, '#938427'], [53, 53, 29, 5, '#351d05'], [21, 140, 67, 96, '#8c4360']]
        j = 0
        k = 0
        b_list = []
        for i in range(int(self.size_squared.text())):
            x_res = 300
            y_res = 300
            x_num = int(int(self.size_squared.text())**0.5)
            y_num = int(int(self.size_squared.text())**0.5)
            b = PicButton(QPixmap('button_off.png'), QPixmap('button_hover.png'), QPixmap('button_on.png'), self)
            width = int(x_res/x_num)
            height = int(y_res/y_num)
            b.setText(str(l[i])), b.setGeometry(k*width, j*width, width, height)
            b.clicked[bool].connect(self.swag)
            k += 1
            if (i+1)/y_num == int((i+1)/y_num):
                j += 1
            if k == x_num:
                k = 0
            b_list.append(b)
        master_list.append(b_list)
        for button in master_list[-1]:
            button.show()
        if len(master_list) > 1:
            for button in master_list[-2]:
                button.hide()
'''

class PreviewFrame(QFrame):
    def __init__(self, color_profile, resolution, photo_res, parent=None):
        super(PreviewFrame, self).__init__(parent)
        sub_win_dim = [350, 150]
        anchor = ""
        # res 1050, 575 : box 350, 150 : window modifier 10, 10 :  color frame dimensions 30, 30
        if color_profile[6] + sub_win_dim[1] + color_profile[8] < resolution[1]:
            anchor += "T"
        else:
            anchor += "B"
        if color_profile[5] + sub_win_dim[0] + color_profile[7] < resolution[0]:
            anchor += "L"
        else:
            anchor += "R"
        print(anchor)

        c = color_profile[1], color_profile[2], color_profile[3]
        self.col = QColor(color_profile[1], color_profile[2], color_profile[3])

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(255, 255, 255))
        self.setPalette(palette)

        hex_value = TextBox(self); rgb = TextBox(self)
        percent = TextBox(self); count = TextBox(self)
        labels = [hex_value, rgb, percent, count]
        x_anchor = 10

        for i in range(len(labels)):
            labels[i].setFont(QFont('Franklin Gothic Medium', 12))
            labels[i].setFrame(False)
            g = [150, 10 + 30*i, 100, 30]
            if i == 1:
                g[2] = 147
            if i > 1:
                g[2] = 200
            labels[i].setGeometry(g[0], g[1], g[2], g[3])
            if "R" in anchor:
                labels[i].setAlignment(Qt.AlignRight)
                x_anchor = sub_win_dim[0] - 10 - 130
                labels[i].setGeometry(sub_win_dim[0] - 10 - 130 - g[2], 10 + 30*i, g[2], g[3])

        hex_value.setText(str(color_profile[4]))
        rgb.setText(str(c))
        percent.setText(str((100*(color_profile[0]/(photo_res[0]*photo_res[1]))).__round__(4)) + "% of the image")
        count.setText(str(color_profile[0]) + " pixels")

        square = QFrame(self)
        square.setGeometry(x_anchor, 10, 130, 130)
        square.setStyleSheet("QWidget { background-color: %s }" % self.col.name())

        # self.setGeometry(300, 300, sub_win_dim[0], sub_win_dim[1])



class Example(QWidget):
    global color_profile, resolution, photo_res, master_list
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        sub_win_dim = [350, 150]
        self.b = QPushButton(self)
        self.b.move(sub_win_dim[0] + 50, 0)
        self.b.clicked.connect(self.change)
        self.s = PreviewFrame(color_profile=color_profile, resolution=resolution, photo_res=photo_res)
        self.s.setGeometry(300, 300, sub_win_dim[0], sub_win_dim[1])
        self.setGeometry(300, 300, sub_win_dim[0] + 100, sub_win_dim[1] + 100)
        self.show()

    def change(self, pressed=None):
        self.s.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

'''
anchor = ""
        # res 1050, 575 : box 350, 150 : window modifier 10, 10 :  color frame dimensions 30, 30
        if color_profile[6] + sub_win_dim[1] + color_profile[8] < resolution[1]:
            anchor += "T"
        else:
            anchor += "B"
        if color_profile[5] + sub_win_dim[0] + color_profile[7] < resolution[0]:
            anchor += "L"
        else:
            anchor += "R"
        print(anchor)

        c = color_profile[1], color_profile[2], color_profile[3]
        self.col = QColor(color_profile[1], color_profile[2], color_profile[3])

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(255, 255, 255))
        self.setPalette(palette)

        hex_value = TextBox(self); rgb = TextBox(self)
        percent = TextBox(self); count = TextBox(self)
        labels = [hex_value, rgb, percent, count]
        x_anchor = 10

        for i in range(len(labels)):
            labels[i].setFont(QFont('Franklin Gothic Medium', 12))
            labels[i].setFrame(False)
            g = [150, 10 + 30*i, 100, 30]
            if i == 1:
                g[2] = 147
            if i > 1:
                g[2] = 200
            labels[i].setGeometry(g[0], g[1], g[2], g[3])
            if "R" in anchor:
                labels[i].setAlignment(Qt.AlignRight)
                x_anchor = sub_win_dim[0] - 10 - 130
                labels[i].setGeometry(sub_win_dim[0] - 10 - 130 - g[2], 10 + 30*i, g[2], g[3])

        hex_value.setText(str(color_profile[4]))
        rgb.setText(str(c))
        percent.setText(str((100*(color_profile[0]/(photo_res[0]*photo_res[1]))).__round__(4)) + "% of the image")
        count.setText(str(color_profile[0]) + " pixels")

        square = QFrame(self)
        square.setGeometry(x_anchor, 10, 130, 130)
        square.setStyleSheet("QWidget { background-color: %s }" % self.col.name())
'''
