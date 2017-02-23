from tkinter import *  # Button, Canvas, PhotoImage, Tk, NORMAL, mainloop
from palette_pull import *  # pulls from palette_pull in palette_work directory
from math import ceil


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


canvas_w = 1200
canvas_h = 700
resolution = "{}".format(str(canvas_w)) + "x{}".format(canvas_h)
master = Tk()
master.geometry(resolution)

w = Canvas(master, width=canvas_w, height=canvas_h)
w.pack()

a_2 = [580, 325, 605, 325, 605, 312, 630, 337, 605, 362, 605, 350, 580, 350]

w.create_rectangle(0, 0, 1200, 700, fill="Pink")
w.create_rectangle(50, 100, 550, 600, fill="White")
w.create_rectangle(650, 100, 1150, 600, fill="White")
a = w.create_polygon(a_2, fill='Maroon')

photo_file = 'ys.gif'
photo = PhotoImage(master=w, file=photo_file)
if photo.width() > 500:
    print("Too Big, running compression... ")
    reduce_to(photo_file)
    photo = PhotoImage(master=w, file='reduced_image.ppm')
w.create_image(300, 350, image=photo)


def callback():

    file_name = photo_file.strip('.gif') + '_grad' + '.gif'
    if photo.width() > 500:
        palette_build(picture_palette('reduced_image.ppm', rgb_range=20, specificity=0.01),
                      x_res=500, y_res=500, native=False, photo_file=photo_file)
    else:
        palette_build(picture_palette(photo_file, rgb_range=20, specificity=0.001),
                      x_res=500, y_res=500, native=False, photo_file=photo_file)

    photo_two = PhotoImage(master=w, file=str(file_name))
    w.create_image(901, 351, image=photo_two, state=NORMAL)


v = Canvas(master=w, width=100, height=100, background='White')
v.pack()
v.create_rectangle(20, 20, 60, 60, fill='Blue')

b = Button(v, text="Sure!", fg='BLue', bg='Orange')
b.pack(fill=NONE, expand=1)

mainloop()
