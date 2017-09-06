import requests
import re


def getImgUrl(url):
    firstImg = ''
    while url != 'null':
        data = requests.get(url).text
        for img in re.findall('"imgUrl":"([^"]*)"', data):
            if img == firstImg:
                return
            firstImg = img if not firstImg else firstImg
            yield "http://stat001.ameba.jp" + img
        url = re.findall('"nextUrl":"([^"]*)"', data)[0]


def getLastEntry(ameba_id):
    url = "http://ameblo.jp/" + ameba_id
    data = requests.get(url).text
    return re.findall("entry-(\d+)\.html", data)[0]


def parse(ameba_id):
    print(ameba_id)
    entry_id = getLastEntry(ameba_id)
    url = ("http://blogimgapi.ameba.jp/read_ahead/get.jsonp?"
           "ameba_id=%s&entry_id=%s&old=true&sp=false" % (ameba_id, entry_id))
    with open(ameba_id, 'w') as file:
        for img in getImgUrl(url):
            file.write(img + '\n')


def test():
    parse('mimorisuzuko')
    # parse('rippi-aloha')
    # parse('pile0502')
    # parse('tokui-sora')
    # parse('aina-heart0201')
    # parse('ichigoshiroppu')


if __name__ == "__main__":
    test()
