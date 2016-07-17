from BeautifulSoup import BeautifulSoup
import datetime
import requests


def program_iter():
    """ yield today's program schedule info"""
    today = datetime.datetime.today()

    url = 'http://www.agqr.jp/timetable/streaming.html'
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text)
    cnt = (today.weekday() + 1) % 7

    rowspan = {}
    idx = 0
    for col in soup.tbody.findAll('td'):
        if not col.text:
            continue

        idx = (idx + 1) % 7
        while idx in rowspan:
            span = rowspan.pop(idx) - 1
            if span:
                rowspan[idx] = span
            idx = (idx + 1) % 7

        if idx == cnt:
            time = col.find('div', {'class': 'time'}).text.lstrip()
            title = col.find('div', {'class': 'title-p'}).text
            if col.find('img', {'src': 'http://cdn-agqr.joqr.jp/schedule/img/icon_m.gif'}):
                title += u' (video)'
            pfm = col.find('div', {'class': 'rp'}).text.split('</span>')[-1]
            try:
                link = col.find('div', {'class': 'title-p'}).a.get('href')
            except:
                link = "None"
            yield (title, time, pfm, link)
        
        if col.get('rowspan'):
            rowspan[idx] = int(col.get('rowspan')) - 1


if __name__ == "__main__":
    for args in program_iter():
        title, time, pfm, link = args
        print "Title:", title
        print "Time:", time
        print "Personality:", pfm
        print "Link:", link
        print ''
