from cImage import *
from math import ceil
import urllib.request
import matplotlib.colors as colors
from PIL import Image


def blah(x, y, z):
    if x + z > y and x - z < y:
        return True
    else:
        return False


def find_duplicate(list):
    new_list = []
    for i in range(len(list)):
        for j in range(len(list)):
            if i != j and list[i] == list[j] and i not in new_list:
                new_list.append(j)
    for a in range(len(new_list)):
        del(list[new_list[a]])
    return list


def blend_region(image, x, y, dim=2):
    rgb = [0, 0, 0]
    for i in range(dim):
        for j in range(dim):
            pixel = image.getPixel(dim*x + i, dim*y + j)
            rgb[0] += pixel.red
            rgb[1] += pixel.green
            rgb[2] += pixel.blue
    for a in range(len(rgb)):
        rgb[a] = int(rgb[a]/(dim**2))
    return rgb


def is_close(rgb_1, rgb_2, ran):
    for i in range(len(rgb_1)):
        if blah(rgb_1[i], rgb_2[i], ran) or blah(sum(rgb_1), sum(rgb_2), 50):
            pass
        else:
            return False
        if i == len(rgb_1) - 1:
            return True


def move_end_to_front(list):
    for j in range(len(list) - 1):
        list.append(list[j])
    del(list[0:3])


def rgb_to_hex(rgb_list):
    return colors.rgb2hex([1.0*x/255 for x in rgb_list])


def last_fm_album_pull(album):
    url = "http://www.lastfm.com/search?q=" + "{}".format(str(album.replace(' ','+')))
    stream = urllib.request.urlopen(url)
    check = 0
    for line in stream:
        line = line.decode("UTF-8")
        if "<h2>Albums</h2>" in line.strip():
            check = 1
        if check == 1:
            if 'src=' in line:
                return str(line.strip().strip('src=').strip('"'))


def nearest_square(number):
    if int(number**0.5) != number**0.5:
        new_number = number
        while int(new_number**0.5) != new_number**0.5:
            new_number += 1
        return new_number
    else:
        return number


def art_pull(album):
    stream = last_fm_album_pull(album)
    url = urllib.request.urlopen(stream)
    output = open("{}".format(str(album)) + ".gif", "wb")
    output.write(url.read())
    output.close()


def resize_image(path):
    basewidth = 300
    img = Image.open(path)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img.save("resized_album.png")


def true_pull(album):
    stream = last_fm_album_pull(album)
    url = urllib.request.urlopen(stream)
    output = open("resized_album.png", "wb")
    output.write(url.read())
    output.close()
    basewidth = 300
    img = Image.open("resized_album.png")
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img.save("resized_album.png")


def picture_palette(file, rgb_range=30, specificity=0.01, uh=3, amount_of_colors='None', fill='Yes'):
    image = FileImage(file)
    area = image.height*image.width
    distinct = [[image.getPixel(0, 0).red, image.getPixel(0, 0).blue, image.getPixel(0, 0).green, 1]]
    distinct_base = []
    check = 0
    while image.width/uh != int(image.width/uh):
        uh += 1
    for x in range(int(image.width/uh)):
        for y in range(int(image.height/uh)):
            test_pixel = image.getPixel(uh*x, uh*y)
            rgb = [test_pixel.red, test_pixel.green, test_pixel.blue]
            rgb = blend_region(image, x, y, dim=uh)
            for i in range(len(distinct)):
                if is_close(rgb, distinct[i], rgb_range):
                    distinct[i][3] += 1*(uh**2)
                    break
                if i == len(distinct) - 1 and not is_close(rgb, distinct[i], rgb_range):
                    rgb.append(1*(uh**2))
                    distinct.append(rgb)
    pre = len(distinct)
    for i in range(len(distinct)):
        move_end_to_front(distinct[i])
        distinct[i].append(rgb_to_hex([distinct[i][1], distinct[i][2], distinct[i][3]]))
    distinct.sort(), distinct.reverse()
    if len(distinct) > int(amount_of_colors):
        del(distinct[int(amount_of_colors):])
    l = nearest_square(len(distinct))
    if fill == "Yes":
        if len(distinct) != l:
            for i in range(l - len(distinct)):
                distinct.append(distinct[i])
    post = len(distinct)
    return distinct, pre, post


def pull_background():
    file = open("C:\\Users\Luke\PycharmProjects\Summer\\palette_config_text.txt", "r")
    for line in file:
        if "bg" in line:
            line = line.replace("bg = [", "").replace("]", "").replace(" ", "")
            bg_list = line.split(",")
            for i in range(3):
                bg_list[i] = int(bg_list[i])
            return bg_list


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return list(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def palette_build(palette, x_res=500, y_res=500, native=True, photo_file=None):
    if not native:
        l = nearest_square(len(palette))
        image = EmptyImage(x_res, y_res)
        for a in range(len(palette)):
            pixel = Pixel(int(palette[a][1]), int(palette[a][2]), int(palette[a][3]))
            for i in range(int(x_res/(l**0.5))):
                x_mod = a*int(x_res/(l**0.5)) - int(a/int((l**0.5)))*int((l**0.5)*int(x_res/(l**0.5))) + i
                for j in range(int(y_res/(l**0.5))):
                    image.setPixel(x_mod, j + int(y_res/(l**0.5))*int(a/(l**0.5)), pixel)
        file_name = 'pal.gif'  # photo_file.strip('.gif') + '_grad'
        image.save(file_name, ftype='gif')


def dec_to_hex(rgb):
    hex_code = '#'
    base = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    for color in rgb:
        for x in range(len(base)):
            for y in range(len(base)):
                if color == 16*x + y:
                    hex_code += "{}".format(base[x]) + "{}".format(base[y])
    return hex_code

