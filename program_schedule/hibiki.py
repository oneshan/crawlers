"""
"""
import datetime
import requests


def program_iter():
    """ yield program info updated today"""
    today = datetime.datetime.today()

    url = "https://vcms-api.hibiki-radio.jp/api/v1//programs"
    payload = {
        "Content-Type": "application/json",
        "Origin": "http://hibiki-radio.jp",
        "X-Requested-With": "XMLHttpRequest",
    }
    weekday = ("mon", "tue", "wed", "thu", "fri", "satsun", "satsun")
    idx = today.weekday()
    params = {'day_of_week': weekday[idx]}
    response = requests.get(url, params=params, headers=payload).json()
    
    for data in response:
        link = "http://hibiki-radio.jp/description/%s/detail" % data['access_id']
        if not data.get('episode'):
            data['episode'] = {'name': None, 'updated_at': data['updated_at']}
        title = u'%s (%s)' % (data['name'], data['episode']['name'])
        pfm = data['cast']
        date = data['episode']['updated_at']
        # pid = data['latest_episode_id']
        if date.split()[0] != today.strftime("%Y/%m/%d"):
            continue
        yield title, pfm, link

if __name__ == "__main__":
    for args in program_iter():
        title, pfm, link = args
        print "Title:", title
        print "Personality:", pfm
        print "Link:", link
        print ''
