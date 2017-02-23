from palette_functions import *
def pull_background():
    file = open("palette_config_text.txt", "r")
    for line in file:
        if "bg" in line:
            line = line.replace("bg = [", "").replace("]", "").replace(" ", "")
            bg_list = line.split(",")
            for i in range(3):
                bg_list[i] = int(bg_list[i])
            return bg_list

