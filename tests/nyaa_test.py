import unittest
import os
import urllib
import feedparser

from animesubs import nyaa
from mock import patch


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
            'subber': u'Commie',
            'anime': u'Sword Art Online',
            'episode': 18,
            'torrent_url': u'http://www.nyaa.eu/?page=download&tid=370091',
        }]

        with patch('animesubs.nyaa.fetch_rss', **self.config):
            result = nyaa.list(1, "Sword Art Online")
            self.assertEquals(result, expected)


if __name__ == "__main__":
    unittest.main()

