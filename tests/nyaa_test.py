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

    def test_search_term_in_url(self):
        config = {'return_value': self.rss}

        with patch('feedparser.parse', **self.config) as mocked:
            nyaa.fetch_rss(1, "Sword Art Online")
            url = mocked.call_args[0][0]
            self.assertTrue('page=rss' in url)
            self.assertTrue('term=Sword+Art+Online' in url)
            self.assertTrue('user=1' in url)
            self.assertTrue(url.startswith("http://nyaa.eu"))


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
        self.submitters = {
            'Commie'       : 1,
            'UTW'          : 2,
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

    def test_one_feed(self):
        config = {
            'submitters': self.submitters,
            'feeds': [
                {
                    'submitter': 'Commie',
                    'search': 'Sword Art Online',
                }
            ]
        }

        expected = [self.sword_art_online]

        with patch('animesubs.nyaa.search', return_value=expected) as mock:
            result = nyaa.from_config(config)
            self.assertEquals(result, expected)
            mock.assert_called_once_with(1, 'Sword Art Online')

    def test_two_feeds(self):
        config = {
            'submitters': self.submitters,
            'feeds': [
                {
                    'submitter': 'Commie',
                    'search': 'Sword Art Online',
                },
                {
                    'submitter': 'UTW',
                    'search': 'Accel World',
                },
            ]
        }

        expected = [[self.sword_art_online], [self.accel_world]]

        with patch('animesubs.nyaa.search', side_effect=expected) as mock:
            result = nyaa.from_config(config)
            print result
            self.assertIn(self.sword_art_online, result)
            self.assertIn(self.accel_world, result)
            calls = mock.call_args_list
            self.assertIn(call(1, 'Sword Art Online'), calls)
            self.assertIn(call(2, 'Accel World'), calls)


if __name__ == "__main__":
    unittest.main()

