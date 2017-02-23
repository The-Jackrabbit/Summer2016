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
    output = open("{}".format(str(album))+ ".gif", "wb")
    output.write(url.read())
    output.close()


def reduce_to(file):
    ys_full = FileImage(file)
    x = 2
    while ys_full.width/x > 500:
        x += 1
    new_res = [int(ys_full.width/x), int(ys_full.height/x)]
    x_multiplier, y_multiplier = int(ceil(ys_full.width/new_res[0])), int(ceil(ys_full.height/new_res[1]))
    new_image = EmptyImage(new_res[0], new_res[1])
    for y in range(int(ys_full.height/y_multiplier)):
        for x in range(int(ys_full.width/x_multiplier)):
            new_pixel = [0, 0, 0]
            oldpixel_one, oldpixel_two, oldpixel_three, oldpixel_four = ys_full.getPixel(x_multiplier*x, y_multiplier*y), ys_full.getPixel(x_multiplier*x + 1, y_multiplier*y), ys_full.getPixel(x_multiplier*x, y_multiplier*y + 1), ys_full.getPixel(x_multiplier*x + 1, y_multiplier*y + 1)
            rgb_one = [oldpixel_one.red, oldpixel_one.green, oldpixel_one.blue]
            rgb_two = [oldpixel_two.red, oldpixel_two.green, oldpixel_two.blue]
            rgb_three = [oldpixel_three.red, oldpixel_three.green, oldpixel_three.blue]
            rgb_four = [oldpixel_four.red, oldpixel_four.green, oldpixel_four.blue]
            new_pixel[0] = int((rgb_one[0] + rgb_two[0] + rgb_three[0] + rgb_four[0])/4)
            new_pixel[1] = int((rgb_one[1] + rgb_two[1] + rgb_three[1] + rgb_four[1])/4)
            new_pixel[2] = int((rgb_one[2] + rgb_two[2] + rgb_three[2] + rgb_four[2])/4)
            n_pixel = Pixel(new_pixel[0], new_pixel[1], new_pixel[2])
            new_image.setPixel(x, y, n_pixel)
    new_image.save('reduced_image', ftype='ppm')


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
    place_holder, x = len(distinct), 0
    l = nearest_square(len(distinct))
    if fill == "Yes":
        if len(distinct) != l:
            for i in range(l - len(distinct)):
                distinct.append(distinct[i])
    post = len(distinct)
    return distinct, pre, post


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
        file_name = 'grad.gif'  # photo_file.strip('.gif') + '_grad'
        image.save(file_name, ftype='gif')


def resize_image(path):
    basewidth = 300
    img = Image.open(path)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img.save("resized_album.png")

