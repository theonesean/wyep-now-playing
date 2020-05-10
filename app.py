import time, sys, requests
import twitter
from requests_html import HTMLSession
from requests_oauthlib import OAuth1, OAuth1Session
from authvars import *

def getNowPlaying():

    try:
        session = HTMLSession()
        r = session.get('http://composer.nprstations.org/widgets/iframe/now.html?station=50e451b6a93e91ee0a00028e')
        r.html.render()
    except:
        print("Error encountered with page render.\n")
        session.close()
        return {
            'song': "",
            'artist': "",
            'program': ""
        }

    s = r.html.find('li.whatson-songTitle', first=True)
    a = r.html.find('li.whatson-songArtist', first=True)
    p = r.html.find('a.whatson-programName', first=True).text

    if s:
        s = s.text
    else:
        s = ""

    if a:
        a = a.text
    else:
        a = ""

    session.close()

    return {
        'song': s,
        'artist': a,
        'program': p
    }

def sendTweet(text):
    if text == None or text == "":
        return

    print("Tweeting: " + text)

    api = twitter.Api(consumer_key=WYEP_CONSUMER_KEY,
                  consumer_secret=WYEP_CONSUMER_SECRET,
                  access_token_key=WYEP_TOKEN,
                  access_token_secret=WYEP_SECRET)
    
    s = api.PostUpdate(text)
    print('Posted tweet "' + s.text + '".')


    # twitter = OAuth1Session(TW_ACCESS_TOKEN,
    #                         client_secret=TW_ACCESS_SECRET,
    #                         resource_owner_key='penis',
    #                         resource_owner_secret='man')

    # url = 'https://api.twitter.com/1.1/statuses/update.json?status=' + requests.utils.quote(text)
    # r = twitter.post(url)

    # print(r.json())

# command line arg will disable tweet on startup
if (len(sys.argv) > 1):
    curr_track = getNowPlaying()
else:
    curr_track = {
        'song': "",
        'artist': "",
        'program': ""
    }

if __name__ == "__main__":
    while True:
        new_track = getNowPlaying()

        if new_track['program'] != curr_track['program'] and new_track['program'] != "":
            sendTweet("Coming up on WYEP: " + new_track['program'])
            time.sleep(5)

        if new_track != curr_track and new_track['song'] != "":
            sendTweet("Now playing: " + new_track['song'] + " by " + new_track['artist'])
            curr_track = new_track
        time.sleep(15)