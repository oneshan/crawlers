from BeautifulSoup import BeautifulSoup
import datetime
import requests


def program_iter():
    """ yield program info updated today"""
    today = datetime.datetime.today()

    url = 'http://www.onsen.ag/index.html?pid=netoge'
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text)
    date = today.strftime('%Y/%m/%d')
    for li in soup.find("div", {"class": "listWrap"}).findAll("li", {"data-update": date}):
        pid = li['id']
        link = 'http://www.onsen.ag/program/%s' % pid
        title = li.h4.text
        pfm = li.find('p', {'class': 'navigator listItem'}).text
        guest = li.get('data-guest', "None")
        yield title, pfm, link, guest


if __name__ == "__main__":
    for args in program_iter():
        title, pfm, link, guest = args
        print "Title:", title
        print "Personality:", pfm
        print "Link:", link
        print "Guest:", guest
        print ''
