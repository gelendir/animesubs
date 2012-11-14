# coding=utf8
import unittest

from animesubs import feeds
from mock import patch


class TestTestFilters(unittest.TestCase):

    def test_empty_feed_empty_entry(self):
        feed = {}
        entry = {}
        expected = True

        result = feeds.test_filters(feed, entry)
        self.assertEquals(result, expected)

    def test_min_episode_under_minimum(self):
        feed = {
            'min_episode': 2
        }
        entry = {
            'subber'    : u'Commie',
            'anime'     : u'Sword Art Online',
            'episode'   : 1,
            'extension' : u'mkv',
        }
        expected = False

        result = feeds.test_filters(feed, entry)
        self.assertEquals(result, expected)

    def test_min_episode_on_minimum(self):
        feed = {
            'min_episode': 2
        }
        entry = {
            'subber'    : u'Commie',
            'anime'     : u'Sword Art Online',
            'episode'   : 2,
            'extension' : u'mkv',
        }
        expected = True

        result = feeds.test_filters(feed, entry)
        self.assertEquals(result, expected)

    def test_min_episode_over_minimum(self):
        feed = {
            'min_episode': 2
        }
        entry = {
            'subber'    : u'Commie',
            'anime'     : u'Sword Art Online',
            'episode'   : 3,
            'extension' : u'mkv',
        }
        expected = True

        result = feeds.test_filters(feed, entry)
        self.assertEquals(result, expected)

    def test_resolution_no_resolution(self):
        feed = {
            'resolution': '720p'
        }
        entry = {
            'subber'    : u'Commie',
            'anime'     : u'Sword Art Online',
            'episode'   : 3,
            'extension' : u'mkv',
        }
        expected = False

        result = feeds.test_filters(feed, entry)
        self.assertEquals(result, expected)

    def test_resolution_invalid_resolution(self):
        feed = {
            'resolution': '720p'
        }
        entry = {
            'subber'    : u'Commie',
            'anime'     : u'Sword Art Online',
            'episode'   : 3,
            'resolution': u'480p',
            'extension' : u'mkv',
        }
        expected = False

        result = feeds.test_filters(feed, entry)
        self.assertEquals(result, expected)

    def test_resolution_right_resolution(self):
        feed = {
            'resolution': '720p'
        }
        entry = {
            'subber'    : u'Commie',
            'anime'     : u'Sword Art Online',
            'episode'   : 3,
            'resolution': u'720p',
            'extension' : u'mkv',
        }
        expected = True

        result = feeds.test_filters(feed, entry)
        self.assertEquals(result, expected)

    def test_no_anime_name(self):
        feed = {
            'anime': 'test'
        }
        entry = {
            'subber'    : u'Commie',
            'episode'   : 3,
            'resolution': u'720p',
            'extension' : u'mkv',
        }
        expected = False

        result = feeds.test_filters(feed, entry)
        self.assertEquals(result, expected)

    def test_wrong_anime_name(self):
        feed = {
            'anime': 'test'
        }
        entry = {
            'subber'    : u'Commie',
            'anime'     : u'Sword Art Online',
            'episode'   : 3,
            'resolution': u'720p',
            'extension' : u'mkv',
        }
        expected = False

        result = feeds.test_filters(feed, entry)
        self.assertEquals(result, expected)

    def test_right_anime_name(self):
        feed = {
            'anime': 'Sword Art Online'
        }
        entry = {
            'subber'    : u'Commie',
            'anime'     : u'Sword Art Online',
            'episode'   : 3,
            'resolution': u'720p',
            'extension' : u'mkv',
        }
        expected = True

        result = feeds.test_filters(feed, entry)
        self.assertEquals(result, expected)

    def test_one_criteria_not_met(self):
        feed = {
            'resolution': '720p',
            'min_episode': 2,
        }
        entry = {
            'subber'    : u'Commie',
            'anime'     : u'Sword Art Online',
            'episode'   : 1,
            'resolution': u'720p',
            'extension' : u'mkv',
        }
        expected = False

        result = feeds.test_filters(feed, entry)
        self.assertEquals(result, expected)

    def test_two_criteria(self):
        feed = {
            'resolution': '720p',
            'min_episode': 2,
        }
        entry = {
            'subber'    : u'Commie',
            'anime'     : u'Sword Art Online',
            'episode'   : 2,
            'resolution': u'720p',
            'extension' : u'mkv',
        }
        expected = True

        result = feeds.test_filters(feed, entry)
        self.assertEquals(result, expected)


class TestFetchEpisodes(unittest.TestCase):

    def test_fetch_episodes(self):
        assert False, "not written yet"


class TestFetchEpisodesFromFeeds(unittest.TestCase):

    def test_fetch_episodes_from_feeds(self):
        assert False, "not written yet"

if __name__ == "__main__":
    unittest.main()