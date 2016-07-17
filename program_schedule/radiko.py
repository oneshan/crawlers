# -*- coding: utf-8 -*-

"""
地域別番組表XML
http://radiko.jp/v2/api/program/today?area_id=[area_id]
http://radiko.jp/v2/api/program/tomorrow?area_id=[area_id]

放送局別週間番組表XML
http://radiko.jp/v2/api/program/station/weekly?station_id=[ID]

放送局XML
http://radiko.jp/v2/station/list/[area_id].xml
"""

from BeautifulSoup import BeautifulSoup
import datetime
import requests

today = datetime.datetime.today()
tomm = today + datetime.timedelta(days=1)

area_mapping = (
    ("JP1", "HOKKAIDO"),
    ("JP2", "AOMORI"),
    ("JP3", "IWATE"),
    ("JP4", "MIYAGI"),
    ("JP5", "AKITA"),
    ("JP6", "YAMAGATA"),
    ("JP7", "FUKUSHIMA"),
    ("JP8", "IBARAKI"),
    ("JP9", "TOCHIGI"),
    ("JP10", "GUNMA"),
    ("JP11", "SAITAMA"),
    ("JP12", "CHIBA"),
    ("JP13", "TOKYO"),
    ("JP14", "KANAGAWA"),
    ("JP15", "NIIGATA"),
    ("JP16", "TOYAMA"),
    ("JP17", "ISHIKAWA"),
    ("JP18", "FUKUI"),
    ("JP19", "YAMANASHI"),
    ("JP20", "NAGANO"),
    ("JP21", "GIFU"),
    ("JP22", "SHIZUOKA"),
    ("JP23", "AICHI"),
    ("JP24", "MIE"),
    ("JP25", "SHIGA"),
    ("JP26", "KYOTO"),
    ("JP27", "OSAKA"),
    ("JP28", "HYOGO"),
    ("JP29", "NARA"),
    ("JP30", "WAKAYAMA"),
    ("JP31", "TOTTORI"),
    ("JP32", "SHIMANE"),
    ("JP33", "OKAYAMA"),
    ("JP34", "HIROSHIMA"),
    ("JP35", "YAMAGUCHI"),
    ("JP36", "TOKUSHIMA"),
    ("JP37", "KAGAWA"),
    ("JP38", "EHIME"),
    ("JP39", "KOUCHI"),
    ("JP40", "FUKUOKA"),
    ("JP41", "SAGA"),
    ("JP42", "NAGASAKI"),
    ("JP43", "KUMAMOTO"),
    ("JP44", "OHITA"),
    ("JP45", "MIYAZAKI"),
    ("JP46", "KAGOSHIMA"),
    ("JP47", "OKINAWA"),
)


def program_iter(area_id="JP13", area_name="TOKYO"):
    """ yield tomorrow's program info"""
    url = 'http://radiko.jp/v2/api/program/tomorrow?area_id=%s' % area_id
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text)

    for station in soup.findAll('station'):
        name = station.find('name').text
        for prog in station.findAll('prog'):
            start_date, start_time = prog['ft'][:-2][:8], prog['ft'][:-2][8:]
            end_time = prog['to'][:-2][8:]
            time = ' %s~%s' % (start_time, end_time)
            if start_date != tomm.strftime("%Y%m%d"):
                time = start_date + time
            title = u'#{0} ({1}) {2}'.format(name, area_name, prog.title.text)
            link = prog.url.text
            pfm = prog.pfm.text
            yield title, time, pfm, link

if __name__ == "__main__":
    for args in program_iter():
        title, time, pfm, link = args
        print "Title:", title
        print "Time:", time
        print "Personality:", pfm
        print "Link:", link
        print ''
