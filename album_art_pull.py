import urllib.request


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


def art_pull(album):
    stream = last_fm_album_pull(album)
    url = urllib.request.urlopen(stream)
    output = open("{}".format(str(album))+ ".gif", "wb")
    output.write(url.read())
    output.close()


art_pull('holy mountain')


