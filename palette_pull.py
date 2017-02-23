from cImage import FileImage, EmptyImage, ImageWin, Pixel


def picture_palette(file, rgb_range=30, specificity=0.01):
    image = FileImage(file)
    area = image.height*image.width
    distinct = [[image.getPixel(0, 0).red, image.getPixel(0, 0).green, image.getPixel(0, 0).blue, 1]]
    for x in range(image.width):
        for y in range(image.height):
            test_pixel = image.getPixel(x, y)
            rgb = [test_pixel.red, test_pixel.green, test_pixel.blue]
            check = 0
            for i in range(len(distinct)):
                if check == 0:
                    if rgb[0] + rgb_range > distinct[i][0] and rgb[0] - rgb_range < distinct[i][0] and rgb[1] + rgb_range > distinct[i][1] and rgb[1] - rgb_range < distinct[i][1] and rgb[2] + rgb_range > distinct[i][2] and rgb[2] - rgb_range < distinct[i][2]:
                        distinct[i][3] += 1
                        check = 1
                    else:
                        if i == len(distinct) - 1:
                            rgb.append(1)
                            distinct.append(rgb)
    z = 0
    while z <= len(distinct) - 1:
        if distinct[z][-1] < specificity*area:
            distinct.remove(distinct[z])
        else:
            z += 1
    return distinct


def nearest_square(number):
    if int(number**0.5) != number**0.5:
        new_number = number
        while int(new_number**0.5) != new_number**0.5:
            new_number += 1
        return new_number
    else:
        return number


def palette_build(palette, x_res=500, y_res=500, native=True, photo_file=None):
    if native:
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
    if not native:
        l = nearest_square(len(palette))
        if len(palette) != l:
            for i in range(l - len(palette)):
                palette.append(palette[i])
        image = EmptyImage(x_res, y_res)
        for a in range(len(palette)):
            for i in range(int(x_res/(l**0.5))):
                for j in range(int(y_res/(l**0.5))):
                    pixel = Pixel(int(palette[a][0]), int(palette[a][1]), int(palette[a][2]))
                    image.setPixel(a*int(x_res/(l**0.5)) - int(a/int((l**0.5)))*int((l**0.5)*int(x_res/(l**0.5))) + i, j + int(y_res/(l**0.5))*int(a/(l**0.5)), pixel)
        file_name = photo_file.strip('.gif') + '_grad'
        image.save(file_name, ftype='gif')


# palette_build(picture_palette('itaots.gif', rgb_range=20, specificity=0.01), x_res=500, y_res=500)


