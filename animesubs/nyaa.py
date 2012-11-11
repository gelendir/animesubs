import urllib
import feedparser
import re

from animesubs.lib import info_from_filename

BASE_URL = "http://nyaa.eu"


def fetch_rss(user_id, term=None):

    params = {
        'page': 'rss',
        'user': user_id,
    }

    if search:
        params['term'] = term

    url = "{0}?{1}".format(BASE_URL, urllib.urlencode(params))
    rss = feedparser.parse(url)

    return rss

def extract_info(entry):
    info = info_from_filename(entry['title'])
    info['torrent_url'] = entry['link']
    info['filename'] = entry['title']
    return info

def search(user_id, term=None):
    rss = fetch_rss(user_id, term)
    anime = [extract_info(e) for e in rss['entries']]
    return anime

def from_config(config):
    submitters = config['submitters']
    episodes = []

    for feed in config['feeds']:
        user_id = submitters[feed['submitter']]
        term = feed['search']
        result = search(user_id, term)
        print result
        episodes.extend(result)

    return episodes
