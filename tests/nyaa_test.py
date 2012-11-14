# coding=utf8
import unittest
import os
import urllib
import feedparser

from animesubs import nyaa
from mock import patch, call


TEST_PATH = os.path.dirname(os.path.abspath(__file__))
RSS = os.path.join(TEST_PATH, 'rss')

class TestFetchRss(unittest.TestCase):

    def setUp(self):
        self.raw_rss = open(os.path.join(RSS, 'commie.rss')).read()
        self.rss = feedparser.parse(self.raw_rss)
        self.config = {'return_value': self.rss}

    def test_fetch_rss(self):
        with patch('feedparser.parse', **self.config) as m:
            result = nyaa.fetch_rss(1)
            self.assertEquals(result, self.rss)
            self.assertIs(type(result['entries'][0]['title']), unicode)

    def test_search_term_in_url(self):
        config = {'return_value': self.rss}

        with patch('feedparser.parse', **self.config) as mocked:
            nyaa.fetch_rss(1, "Sword Art Online")
            url = mocked.call_args[0][0]
            self.assertIn('page=rss',  url)
            self.assertIn('term=Sword+Art+Online',  url)
            self.assertIn('user=1', url)
            self.assertTrue(url.startswith("http://nyaa.eu"))

    def test_search_term_unicode(self):
        config = {'return_value': self.rss}
        with patch('feedparser.parse', **self.config) as mocked:
            nyaa.fetch_rss(1,  u"「K」")
            url = mocked.call_args[0][0]
            self.assertIn(u'term=%E3%80%8CK%E3%80%8D',  url)


class TestListAnime(unittest.TestCase):

    def setUp(self):
        path = os.path.join(RSS, 'commie_sword_art_online_18.rss')
        self.rss = feedparser.parse(path)
        self.config = {'return_value': self.rss}

    def test_fetch_anime_list(self):

        expected = [{
            'subber'      : u'Commie',
            'anime'       : u'Sword Art Online',
            'episode'     : 18,
            'crc32'       : u'F440EE69',
            'extension'   : u'mkv',
            'torrent_url' : u'http://www.nyaa.eu/?page=download&tid=370091',
            'filename'    : '[Commie] Sword Art Online - 18 [F440EE69].mkv',
        }]

        with patch('animesubs.nyaa.fetch_rss', **self.config):
            result = nyaa.search(1, "Sword Art Online")
            self.assertEquals(result, expected)

class TestFromConfig(unittest.TestCase):

    def setUp(self):
        self.log_patcher = patch.object(nyaa.logger, 'info')
        self.log_patcher.start()

        self.submitters = {
            'Commie'       : 1,
            'UTW'          : 2,
            'sage-koi'     : 3,
        }

        self.sword_art_online = {
            'subber'      : u'Commie',
            'anime'       : u'Sword Art Online',
            'episode'     : 18,
            'crc32'       : u'F440EE69',
            'extension'   : u'mkv',
            'torrent_url' : u'http://www.nyaa.eu/?page=download&tid=370091',
            'filename'    : '[Commie] Sword Art Online - 18 [F440EE69].mkv',
        }

        self.accel_world = {
            'subber'      : u'UTW',
            'anime'       : u'Accel World',
            'episode'     : 24,
            'crc32'       : u'1DF1511D',
            'extension'   : u'mkv',
            'torrent_url' : u'http://www.nyaa.eu/?page=download&tid=354607',
            'filename'    : '[UTW]_Accel_World_-_24_[h264-720p][1DF1511D].mkv',
        }

        self.code_breaker = {
            'subber'      : u'sage-koi',
            'anime'       : u'CØDE：BREAKER',
            'episode'     : 3,
            'crc32'       : u'735482AF',
            'extension'   : u'mkv',
            'torrent_url' : u'http://www.nyaa.eu/?page=download&tid=354607',
            'filename'    : u'[sage-koi]_CØDE：BREAKER_-_03_[720p][10bit][735482AF].mkv'
        }

    def tearDown(self):
        self.log_patcher.stop()

    def test_feed_one_episode(self):
        config = {
            'submitters': self.submitters,
        }
        feed = {
            'submitter': 'Commie',
            'search': 'Sword Art Online',
        }
        search_result = [self.sword_art_online]
        expected = [self.sword_art_online]

        with patch('animesubs.nyaa.search', return_value=search_result) as mocked:
            result = nyaa.fetch_feed(feed, config)

            self.assertEquals(result, expected)
            mocked.assert_called_once_with(1, 'Sword Art Online')

    def test_feed_unicode_episode(self):
        config = {
            'submitters': self.submitters,
        }
        feed = {
            'submitter': u'sage-koi',
            'search': u'CØDE：BREAKER',
        }
        search_result = [self.code_breaker]
        expected = [self.code_breaker]

        with patch('animesubs.nyaa.search', return_value=search_result) as mocked:
            result = nyaa.fetch_feed(feed, config)

            self.assertEquals(result, expected)
            mocked.assert_called_once_with(3, u'CØDE：BREAKER')

    def test_feed_two_episodes(self):
        config = {
            'submitters': self.submitters
        }
        feed = {
            'submitter': 'Commie',
            'search': 'various',
        }
        search_result = [self.sword_art_online, self.code_breaker]
        expected = [self.sword_art_online, self.code_breaker]

        with patch('animesubs.nyaa.search', return_value=search_result) as mocked:
            result = nyaa.fetch_feed(feed, config)

            self.assertEquals(result, expected)
            mocked.assert_called_once_with(1, u'various')


if __name__ == "__main__":
    unittest.main()

