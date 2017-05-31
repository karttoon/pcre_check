from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json

__author__  = "Jeff White [karttoon] @noottrak"
__email__   = "karttoon@gmail.com"
__version__ = "1.0.0"
__date__    = "31MAY2017"

# Output for use with pcre_check
# Fill out your API keys

access_token        = ""
access_token_secret = ""
consumer_key        = ""
consumer_secret     = ""

def url_proc(url_mod):

    if "http" not in url_mod:
        url_mod = "http://" + url_mod
    if "twitter.com" not in url_mod and \
        "twimg.com" not in url_mod and \
        "t.co" not in url_mod and \
        "fb.me" not in url_mod and \
        "ift.tt" not in url_mod and \
        "youtu.be" not in url_mod and \
        "bit.ly" not in url_mod and \
        "google.com" not in url_mod and \
        "facebook.com" not in url_mod and \
        "du3a.org" not in url_mod and \
        "d3waapp.org" not in url_mod and \
        "buff.ly" not in url_mod and \
        "goo.gl" not in url_mod and \
        "ow.ly" not in url_mod and \
        "tinyurl.com" not in url_mod and \
        "dlvr.it" not in url_mod and \
        "ghared.com" not in url_mod and \
        "zad-muslim.com" not in url_mod and \
        "bnent.jp" not in url_mod and \
        "max335.com" not in url_mod and \
        "fllwrs.com" not in url_mod and \
        "7asnh.com" not in url_mod and \
        "twcm.me" not in url_mod and \
        "cas.st" not in url_mod and \
        "dld.bz" not in url_mod and \
        "nico.ms" not in url_mod and \
        "paper.li" not in url_mod and \
        "ebay.com" not in url_mod and \
        "ameblo.jp" not in url_mod and \
        "totodio.com" not in url_mod and \
        "wp.me" not in url_mod and \
        "amzn.to" not in url_mod and \
        "naver.me" not in url_mod and \
        "prt.nu" not in url_mod and \
        "ask.fm" not in url_mod and \
        "youtube.com" not in url_mod and \
        "etsy.me" not in url_mod and \
        "trib.al" not in url_mod and \
        "getm.pt" not in url_mod and \
        "bigo.sg" not in url_mod and \
        "dictionaryvoice.com" not in url_mod:
        
        print url_mod

    return

class StdOutListener(StreamListener):

    def on_data(self, data):
        urls = []

        data = json.loads(data)
        try:
            urls.append(data['entities']['urls'][0]['expanded_url'])
            urls.append(data['entities']['urls'][0]['url'])
        
            for url in urls:
                url_proc(url)     
        except:
            pass
                
        # re.findall("((http(s)?:\\\/\\\/)?([a-zA-Z0-9.-]+)+\.[a-zA-Z.]{2,6}\\\/([a-zA-Z0-9\\\/.+=?%])+)+", data):

        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':

    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track=['http'])
