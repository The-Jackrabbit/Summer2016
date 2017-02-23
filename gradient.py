from cImage import *
from math import ceil
import random

def list_of_colors(code_type='rgb'):
    library = []
    file_name = 'pastel_library_{}'.format(code_type) + '.txt'
    file = open(file_name, 'r')
    if code_type == 'rgb':
        for line in file:
            line = line.strip('\n').strip('[').strip(']').replace(' ', '')
            rgb = line.split(',')
            rgb[0], rgb[1], rgb[2] = int(rgb[0]), int(rgb[1]), int(rgb[2])
            library.append(rgb)
    else:
        for line in file:
            library.append(str(line.strip('\n')))
    return library


lib = list_of_colors('rgb')


def gradient(canvas, rgb_1, rgb_2, canvas_width, canvas_height, dire='y', option='normal'):
    lol = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    print(lol[0])
    r_dif = rgb_2[0] - rgb_1[0]
    g_dif = rgb_2[1] - rgb_1[1]
    b_dif = rgb_2[2] - rgb_1[2]
    if option == 'normal':
        if dire == 'y':
            r, c = canvas_height, canvas_width
        else:
            c, r = canvas_height, canvas_width
        for row in range(r):
            ratio = row/canvas_height
            pixel = Pixel(rgb_1[0] + int(r_dif*ratio), rgb_1[1] + int(g_dif*ratio), rgb_1[2] + int(b_dif*ratio))
            for col in range(c):
                if dire == 'y':
                    canvas.setPixel(col, row, pixel)
                else:
                    canvas.setPixel(row, col, pixel)
        return canvas
    if option == 'matrix':
        # size = self.size.text()
        size = 2

        num = size**2
        palette = []
        square_length = canvas_width/size
        if square_length - .5 < int(square_length):
            square_length = int(square_length)
        else:
            square_length = int(square_length)
        if square_length*size != canvas_width:
            print(square_length*size)
            print(canvas_width)
            print('check')
        else:
            print(square_length*size)
            print(canvas_width)

        for i in range(size):
            for j in range(size):
                profile = [int(rgb_1[0] + len(palette)*r_dif/num), int(rgb_1[1] + len(palette)*g_dif/num),
                           int(rgb_1[2] + len(palette)*b_dif/num), square_length*j, square_length*i]
                palette.append(profile)
        print(palette)
        for k in range(len(palette)):
            for a in range(square_length):
                for b in range(square_length):
                    pixel = Pixel(palette[k][0], palette[k][1], palette[k][2])
                    canvas.setPixel(palette[k][3] + b, palette[k][4] + a, pixel)
        return canvas


def run_gradient(rgb_library):
    color_one = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
    color_two = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
    while abs(sum(color_one) - sum(color_two)) < 150:
        color_two = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
    # color_one = [11, 85, 242]
    # color_two = [247, 159, 215]
    print(color_one)
    print(color_two)
    x_res, y_res = 300, 300
    old_image = EmptyImage(x_res, y_res)
    image_window = ImageWin("Image Processing", x_res, y_res)
    image = gradient(old_image, color_one, color_two, x_res, y_res, dire='y', option='normal')
    image.draw(image_window)
    image_window.exitOnClick()
    save = str(input("Save?(y/n): "))
    file_name = str(color_one) + str(color_two)
    if save != 'n':
        image.save('C:\\Users\Luke\PycharmProjects\Summer\Palette Work\Gradients\\' + file_name, ftype='png')



run_gradient(lib)
