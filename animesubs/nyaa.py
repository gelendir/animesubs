import feedparser
import logging
import re
import urllib

from animesubs.lib import info_from_filename

BASE_URL = "http://nyaa.eu"

logger = logging.getLogger(__name__)


def fetch_rss(user_id, term=None):

    params = {
        'page': 'rss',
        'user': user_id,
    }

    if term:
        params['term'] = term.encode('utf8')

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
        logger.info("fetching %s %s", feed['submitter'], feed['search'])

        user_id = submitters[feed['submitter']]
        term = feed['search']
        entries = search(user_id, term)
        episodes.extend(entries)

    return episodes
