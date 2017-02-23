import urllib.request
import re


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return list(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def execute_pastel_pull():
    catalog = [[2015, 13], [2016, 6]]
    for i in range(len(catalog)):
        for j in range(1, catalog[i][1]):
            hex_file = open("pastel_library_hex.txt", "a")
            rgb_file = open("pastel_library_rgb.txt", "a")
            url = 'http://automaticpastels.tumblr.com/archive/{}'.format(str(catalog[i][0])) + '/{}'.format(j)
            stream = urllib.request.urlopen(url)
            for line in stream:
                line = line.decode("UTF-8")
                pastel_compiler = re.compile(r'[a-z0-9][a-z0-9][a-z0-9][a-z0-9][a-z0-9][a-z0-9]"><div class="hover_inner">')
                pastel_regex = pastel_compiler.findall(line)
                if len(pastel_regex) != 0:
                    hxdc = '#' + pastel_regex[0].replace('"><div class="hover_inner">', '')
                    hex_file.write(hxdc + '\n')
                    rgb_file.write('{}'.format(hex_to_rgb(hxdc)) + '\n')
            hex_file.close()
            rgb_file.close()


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


execute_pastel_pull()
