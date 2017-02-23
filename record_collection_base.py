import re
import urllib.request

# https://www.discogs.com/search/?q=meat+is+murder&type=all


def pull_result_list(search_term):
    url_search_term = str(search_term.lower().replace(" ", "+"))
    url = "https://www.discogs.com/search/?q=" + url_search_term + "&type=all"
    print(url)
    stream = urllib.request.urlopen(url)
    for line in stream:
        line = line.decode("UTF-8")
        if '<h4><a href="' in line:
            url_regex = re.compile(r"[A-Za-z0-9/-]+")
            url_compiler = url_regex.findall(line)
            if len(url_compiler) != 0:
                print(url_compiler[0])


pull_result_list("meat is murder")