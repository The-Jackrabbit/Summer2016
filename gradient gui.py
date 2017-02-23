from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
from palette_functions import picture_palette, nearest_square, resize_image, true_pull
from cImage import *
from palette_config import *


class PicButton(QAbstractButton):
    def __init__(self, pixmap, pixmap_pressed, pixmap_hover, parent=None):
        super(PicButton, self).__init__(parent)
        self.setMouseTracking(True)
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


class CheckButton(QAbstractButton):
    def __init__(self, pixmap, pixmap_pressed, parent=None):
        super(CheckButton, self).__init__(parent)
        self.setMouseTracking(True)
        self.pixmap = pixmap
        self.pixmap_pressed = pixmap_pressed
        self.pressed.connect(self.update)
        self.released.connect(self.update)

    def paintEvent(self, event):
        pix = self.pixmap
        if self.isChecked():
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
        bgc = QColor(background[0], background[1], background[2])
        pal.setColor(QPalette.Base, bgc)
        textc = QColor(4, 0, 53)
        pal.setColor(QPalette.Text, textc)
        self.setPalette(pal)


class PreviewFrame(QFrame):
    def __init__(self, color_profile, resolution, photo_res, parent=None):
        super(PreviewFrame, self).__init__(parent)
        sub_win_dim = [350, 150]
        anchor = ""
        if color_profile[6] + sub_win_dim[1] + color_profile[8] < resolution[1]:
            anchor += "T"
        else:
            anchor += "B"
        if color_profile[5] + sub_win_dim[0] < resolution[0]:
            anchor += "L"
        else:
            anchor += "R"

        c = color_profile[1], color_profile[2], color_profile[3]
        self.col = QColor(color_profile[1], color_profile[2], color_profile[3])
        self.bcol = QColor(255, 255, 255)
        self.setStyleSheet("QWidget { background-color: %s }" % self.bcol.name())

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
        percent.setText(str((100*(color_profile[0]/(photo_res[0]*photo_res[1]))).__round__(2)) + "% of the image")
        count.setText(str(color_profile[0]) + " pixels")

        square = QFrame(self)
        square.setGeometry(x_anchor, 10, 130, 130)
        square.setStyleSheet("QWidget { background-color: %s }" % self.col.name())
        self.exit_button = PicButton(QPixmap("C:\\Users\Luke\PycharmProjects\Summer\Palette Work\Icons\\x.png"),
                                     QPixmap("C:\\Users\Luke\PycharmProjects\Summer\Palette Work\Icons\\x.png"),
                                     QPixmap("C:\\Users\Luke\PycharmProjects\Summer\Palette Work\Icons\\x.png"), self)
        if "L" in anchor:
            self.exit_button.setGeometry(sub_win_dim[0] - 30, 10, 20, 20)
        if "R" in anchor:
            self.exit_button.setGeometry(10, 10, 20, 20)
        x = color_profile[5] - 10
        y = color_profile[6] - 10
        if anchor == "TR":
            x = color_profile[5] - sub_win_dim[0] + color_profile[-2]
        if anchor == "BL":
            y = color_profile[6] - sub_win_dim[1] + color_profile[-1]
        if anchor == "BR":
            x = color_profile[5] - sub_win_dim[0] + color_profile[-2]
            y = color_profile[6] - sub_win_dim[1] + color_profile[-1]
        self.setGeometry(x, y, sub_win_dim[0], sub_win_dim[1])
        self.exit_button.clicked[bool].connect(self.close_frame)

    def close_frame(self):
        for item in preview_list:
            item.hide()


class Example(QWidget):
    ran = 30

    def __init__(self):
        super().__init__()
        self.initialize_ui()

    def initialize_ui(self):

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(background[0], background[1], background[2])), self.setPalette(palette)
        textc = QColor(4, 0, 53)
        palette.setColor(QPalette.Text, textc)
        self.afp = TextBox(self); self.range = TextBox(self); self.noc = TextBox(self)
        self.pre_count = TextBox(self); self.post_count = TextBox(self); self.density_control = TextBox(self); self.fill = TextBox(self)

        self.album = QLabel(self); self.grad = QLabel(self); album_frame = QLabel(self); self.fill_label = QLabel("Fill?: ", self)
        palette_frame = QLabel(self); self.range_label = QLabel("RGB Range", self); self.nocl = QLabel("2x2", self)
        self.pre_count_label = QLabel("Unique Colors", self); self.post_count_label = QLabel("# of Squares", self); self.dcl = QLabel("Density Control", self)

        self.density_control.setGeometry(480, 280, 80, 35), self.density_control.setFrame(False)
        self.density_control.setText("2"), self.density_control.setFont(QFont('Franklin Gothic Medium', 12))
        self.dcl.setGeometry(480, 255, 88, 35)
        if self.density_control.text() != '':
            self.density_control.returnPressed.connect(self.pull_image)

        album_picture = QPixmap()

        self.album.setPixmap(album_picture)
        self.album.setGeometry(138, 138, 300, 300), self.fill.setGeometry(478, 230, 80, 35)
        self.grad.setGeometry(613, 138, 300, 300), self.fill_label.setGeometry(480, 205, 80, 35)
        self.afp.setGeometry(100, 50, 375, 50), self.range.setGeometry(480, 115, 80, 35)
        self.range_label.setGeometry(480, 90, 90, 35)

        self.switch = CheckButton(QPixmap('C:\\Users\Luke\PycharmProjects\Summer\Palette Work\Icons\\on.png'),
                                  QPixmap('C:\\Users\Luke\PycharmProjects\Summer\Palette Work\Icons\\off.png'), self)
        self.switch.setCheckable(True)
        self.switch.setGeometry(478, 232, 90, 30)
        self.fill.setText("Yes"), self.fill.setFrame(False)
        self.switch.clicked[bool].connect(self.mutate_fill)
        if self.fill.text() != '':
            self.fill.returnPressed.connect(self.pull_image)
        self.fill.setFont(QFont('Franklin Gothic Medium', 12))

        frame_two = QPixmap("C:\\Users\Luke\PycharmProjects\Summer\Palette Work\Icons\\album_f.png")
        palette_frame.setPixmap(frame_two)
        palette_frame.move(575, 100)

        self.menu = QComboBox(self)
        self.menu.addItem("2x2"), self.menu.addItem("3x3"), self.menu.addItem("4x4"), \
        self.menu.addItem("5x5"), self.menu.addItem("6x6"), self.menu.addItem("12x12")
        self.menu.addItem("17x17")
        self.menu.move(50, 50)
        self.menu.activated[str].connect(self.mutate)
        self.menu_label = QLabel("Box Size", self)
        self.menu_label.setGeometry(480, 150, 80, 35)

        self.afp.setText("to be kind"), self.afp.setFrame(False)
        self.afp.setFont(QFont('Franklin Gothic Medium', 20))
        if self.afp.text() != '':
            self.afp.returnPressed.connect(self.pull_image)

        self.range.setText('30')
        self.range.setFont(QFont('Franklin Gothic Medium', 12))
        if self.afp.text() != '':
            self.range.returnPressed.connect(self.pull_image)
        self.menu.setGeometry(478, 180, 80, 25)

        self.pre_count.setFont(QFont('Franklin Gothic Medium', 12))
        self.pre_count.setText('')
        self.pre_count.setGeometry(480, 340, 80, 35), self.pre_count_label.setGeometry(480, 310, 80, 35)

        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(675, 485, 280, 30)

        self.go = QPushButton("Go", self)
        self.go.setGeometry(500, 485, 30, 30)
        if self.afp.text() != '':
            self.go.clicked.connect(self.pull_image)

        self.post_count.setFont(QFont('Franklin Gothic Medium', 12))
        self.post_count.setText('')
        self.post_count.setGeometry(480, 410, 80, 35), self.post_count_label.setGeometry(480, 380, 80, 35)
        self.range.setFrame(False), self.noc.setFrame(False), self.pre_count.setFrame(False), self.post_count.setFrame(False)
        self.setGeometry(300, 300, 1050, 575)
        self.setWindowTitle('Album Palettes')
        self.setWindowIcon(QIcon('palette_build_icon_full.png'))
        self.show()

    def save_image(self):
        album = self.afp.text()
        album_image = FileImage("resized_album.png")
        album_image.save("C:\\Users\Luke\PycharmProjects\Summer\Palette Work\Albums\\{}".format(album) + ".png")
        f_name = "C:\\Users\Luke\PycharmProjects\Summer\Palette Work\Albums\\{}".format(album) + \
                 "_" + self.range.text() + "_" + self.nocl.text() + "_grad.png"
        self.palette_build_two(g_distinct, x_res=1000, y_res=1000, file_name=f_name)
        self.save_image_button.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())