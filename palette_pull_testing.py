from cImage import *


def nearest_square(number):
    if int(number**0.5) != number**0.5:
        new_number = number
        while int(new_number**0.5) != new_number**0.5:
            new_number += 1
        return new_number
    else:
        return number


def palette_build(palette, x_res=500, y_res=500):
    l = nearest_square(len(palette))
    if len(palette) != l:
        for i in range(l - len(palette)):
            palette.append(palette[i])
    image = EmptyImage(x_res, y_res)
    image_window = ImageWin('Palette', x_res, y_res)
    for a in range(len(palette)):
        for i in range(int(x_res/(l**0.5))):
            for j in range(int(y_res/(l**0.5))):
                pixel = Pixel(int(palette[a][0]), int(palette[a][1]), int(palette[a][2]))
                image.setPixel(a*int(x_res/(l**0.5)) - int(a/int((l**0.5)))*int((l**0.5)*int(x_res/(l**0.5))) + i, j + int(y_res/(l**0.5))*int(a/(l**0.5)), pixel)
    image.draw(image_window)
    image_window.exitonclick()
    file_name = str(input("File name?: "))
    image.save(file_name, ftype='gif')


