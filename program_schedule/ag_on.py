# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
import datetime
import requests


def program_iter():
    """ yield program info updated today"""
    today = datetime.datetime.today()

    url = 'http://ondemand.joqr.co.jp/AG-ON/contents/newarrival.php'
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text)

    for row in soup.find('div', {'id': 'right'}).findAll('li'):
        link = row.a.get('href')
        date = row.p.contents[0].text
        title = row.p.contents[2].lstrip()
        pfm = row.p.contents[-1].lstrip().split(u'：')[-1]
        if today.strftime('%Y.%m.%d') != date:
            continue
        yield title, pfm, link


if __name__ == "__main__":
    for args in program_iter():
        title, pfm, link = args
        print "Title:", title
        print "Personality:", pfm
        print "Link:", link
        print ''
