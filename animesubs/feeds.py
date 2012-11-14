import logging
import os
import urllib

from animesubs import nyaa

logger = logging.getLogger(__name__)


def test_filters(feed, entry):
    min_episode = feed.get('min_episode')
    if min_episode and not (entry.get('episode', 0) >= min_episode):
        return False

    resolution = feed.get('resolution')
    if resolution and not (resolution == entry.get('resolution')):
        return False

    anime = feed.get('anime')
    if anime and not(anime == entry.get('anime')):
        return False

    return True

def fetch_episodes(feedtype, feed, feedconfig):
    if feedtype == "nyaa":
        return nyaa.fetch_feed(feed, feedconfig)

def fetch_episodes_from_feeds(config):
    all_episodes = []

    for feedtype, feedconfig in config.iteritems():
        feeds = feedconfig.pop('feeds')
        for feed in feeds:
            episodes = (
                e for e in fetch_episodes(feedtype, feed, feedconfig)
                if test_filters(feed, e)
            )
            all_episodes.extend(episodes)

    return all_episodes

