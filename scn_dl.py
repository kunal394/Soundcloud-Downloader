#!/usr/bin/env python

"""download url for any track will be of the form:
    https://cf-media.sndcdn.com/Km8dsbZTyez0.128.mp3?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiKjovL2NmLW1lZGlhLnNuZGNkbi5jb20vS204ZHNiWlR5ZXowLjEyOC5tcDMiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE0NTI3NjMzNDZ9fX1dfQ__&Signature=WKX602uwXoYowQaPuh5BxSU~Uo8LIIQd1ZLj-n-rS34Y7IdNJLWHfQuRnx8AG4hK922I1b5QzCXWOKUH6UrTG2mN8D0fd4ghR2DJDwfdwhPtW1p5uZUTnDRADk~ciBIZnOFrWlF~GfapXjPTwQLQXRhNJiBttAGY15qRF92wlYWlRSJ5zcWmLK4pz5fwgI7xyFg52gYC7xis8sSTkJ5TOAS5daVwMDVmO2lNdYuJO2JOEX0kyCUgO6oJj7xh3taQZk-EUfIaABtXlk3ExfKdD1IvisLlTLVjpUseAusLwDlwdSLO~6b5Mj5A18nLf-UpK-BxNQI4i1vrKrkAbXwVmw__&Key-Pair-Id=APKAJAGZ7VMH2PFPW6UQ

    which is obtained from a url of type:
    https://api.soundcloud.com/i1/tracks/211536794/streams?client_id=02gUJC0hH2ct1EGOcYXQIzRFU91c72Ea&app_version=8711825
    so we need to get three variables for obtaining the location of any track:
     1. track_id: tracks/211536794
     2. client_id
     3. app_version

     and then construct the an url similar to the one shown above.
     """

import requests, re, json, argparse, codecs
from bs4 import BeautifulSoup

def fetch_download_url(song):
    r = requests.get(song)
    s = BeautifulSoup(r.text, 'html.parser')
    #get the app_version
    app_version = re.compile('window.__sc_version = ".*";').search(s.text).group(0)
    app_version=str(re.search('".*"',app_version).group(0))[1:][:-1]
    #get the track_id
    track_id = re.compile('tracks:\d*"').search(s.text).group(0)
    #re.sub("regex_str", "string_to_replace", "string to perform regex on")
    track_id = str(re.sub('\D*', '', track_id))
    client_id = "02gUJC0hH2ct1EGOcYXQIzRFU91c72Ea"
    fetch_url = "https://api.soundcloud.com/i1/tracks/"+track_id+"/streams?client_id="+client_id+"&app_version="+app_version
    r = requests.get(fetch_url)
    j = json.loads(r.text)
    download_url = j['http_mp3_128_url']
    return download_url

def download_song(url):
    download_url = fetch_download_url(url)
    song_name = re.sub('-', ' ', url.split('?')[0].split('/')[-1]).title()
    song_file = song_name + ".mp3"
    with open(song_file, 'wb')  as f:
        data = requests.get(download_url, stream = True)
        for chunk in data.iter_content(chunk_size=1024*1024):
            if chunk:
                print "len: ",len(chunk)
                f.write(chunk)
        f.close()
        return data        


#first download:https://soundcloud.com/lanksmusic/lanks-brothers-of-the-mountain?in=lanksmusic/sets/lanks-banquet-ep-2015

if __name__ == "__main__":
    if (int(requests.__version__[0]) == 0):
        print ("Your version of requests needs updating\nTry: '(sudo) pip install -U requests'")
        sys.exit()
    
    #argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help = "increase output verbosity", action = "store_true")
    parser.add_argument("music_url", help = "Soundcloud Song URL")
    args = parser.parse_args()
    verbose = bool(args.verbose)
    download_song(args.music_url)
