import logging
import os
import urllib

from animesubs import nyaa

logger = logging.getLogger(__name__)


def test_filters(config, entry):
    min_episode = config.get('min_episode')
    if min_episode and not (entry.get('episode', 0) >= min_episode):
        return False

    resolution = config.get('resolution')
    if resolution and not (resolution == entry.get('resolution')):
        return False

    anime = config.get('anime')
    if anime and not(anime == entry.get('anime')):
        return False

    return True

def fetch_entries(feedtype, feedconfig):
    if feedtype == "nyaa":
        return nyaa.from_config(feedconfig)

def fetch_feeds(feeds):
    all_anime = []

    for feedtype, feedconfig in feeds:
        entries = (
            x for x in fetch_entries(feedtype, feedconfig)
            if test_filters(feedconfig, x)
        )
        all_anime.extend(entries)

    return anime

