import math
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    list(int(value[i:i + lv // 3], 16)
    for i in range(0, lv, lv // 3))


'''
R/16 = x + y/16
G/16 = x' + y'/16
B/16 = x" + y"/16
'''

# [175, 236, 205][27, 84, 91].ppm


def dec_to_hex(rgb):
    hex_code = '#'
    base = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    for color in rgb:
        for x in range(len(base)):
            for y in range(len(base)):
                if color == 16*x + y:
                    hex_code += "{}".format(base[x]) + "{}".format(base[y])
    return hex_code


print(dec_to_hex([27, 84, 91]))
