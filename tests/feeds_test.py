# coding=utf8
import unittest

from animesubs import feeds, nyaa
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

    def setUp(self):
        self.nyaa_result = [{
            'subber'    : u'Commie',
            'anime'     : u'Sword Art Online',
            'episode'   : 2,
            'resolution': u'720p',
            'extension' : u'mkv',
        }]

    @patch('animesubs.nyaa.fetch_feed')
    def test_fetch_episodes(self, mocked):
        feed = {
            'submitter': 'Commie',
            'search': 'Sword Art Online',
        }
        feedconfig = {
            'submitters': {
                'Commie': 1,
            },
        }

        mocked.return_value = self.nyaa_result

        result = feeds.fetch_episodes("nyaa", feed, feedconfig)
        mocked.asset_called_once_with(feed, feedconfig)

class TestFilterEpisodeVersions(unittest.TestCase):

    def test_filter_empty_list(self):
        episodes = []
        expected = []

        result = feeds.filter_episode_versions(episodes)
        self.assertEquals(result, expected)

    def test_filter_one_episode_no_version(self):
        episodes = [
            {
                'anime': u"Mâgì",
                'episode': 1,
            }
        ]
        expected = episodes

        result = feeds.filter_episode_versions(episodes)
        self.assertEquals(result, expected)

    def test_filter_one_episode_with_version(self):
        episodes = [
            {
                'anime': u"Mâgì",
                'episode': 1,
                'version': 2,
            }
        ]
        expected = episodes

        result = feeds.filter_episode_versions(episodes)
        self.assertEquals(result, expected)

    def test_filter_two_episodes_with_version(self):
        episodes = [
            {
                'anime': u"Mâgì",
                'episode': 1,
                'version': 2,
            },
            {
                'anime': u"Mâgì",
                'episode': 2,
                'version': 2,
            }
        ]
        expected = episodes

        result = feeds.filter_episode_versions(episodes)
        self.assertEquals(result, expected)

    def test_filter_same_episode_two_versions(self):
        episodes = [
            {
                'anime': u"Mâgì",
                'episode': 1,
                'version': 1,
            },
            {
                'anime': u"Mâgì",
                'episode': 1,
                'version': 2,
            }
        ]
        expected = [
            {
                'anime': u"Mâgì",
                'episode': 1,
                'version': 2,
            }
        ]

        result = feeds.filter_episode_versions(episodes)
        self.assertEquals(result, expected)

    def test_filter_same_episode_one_version(self):
        episodes = [
            {
                'anime': u"Mâgì",
                'episode': 1,
            },
            {
                'anime': u"Mâgì",
                'episode': 1,
                'version': 2,
            }
        ]
        expected = [
            {
                'anime': u"Mâgì",
                'episode': 1,
                'version': 2,
            }
        ]

        result = feeds.filter_episode_versions(episodes)
        self.assertEquals(result, expected)

    def test_filter_two_anime(self):
        episodes = [
            {
                'anime': u"Mâgì",
                'episode': 1,
            },
            {
                'anime': u"Àccel wôrld",
                'episode': 1,
            }
        ]
        expected = list(episodes)

        result = feeds.filter_episode_versions(episodes)
        self.assertEquals(sorted(result), sorted(expected))

    def test_filter_two_anime_one_version(self):
        episodes = [
            {
                'anime': u"Mâgì",
                'episode': 1,
            },
            {
                'anime': u"Àccel wôrld",
                'episode': 1,
                'version': 2,
            }
        ]
        expected = list(episodes)

        result = feeds.filter_episode_versions(episodes)
        self.assertEquals(sorted(result), sorted(expected))

    def test_filter_two_anime_two_versions(self):
        episodes = [
            {
                'anime': u"Àccel wôrld",
                'episode': 1,
                'version': 2,
            },
            {
                'anime': u"Mâgì",
                'episode': 1,
            },
            {
                'anime': u"Àccel wôrld",
                'episode': 1,
                'version': 1,
            },
        ]
        expected = [
            {
                'anime': u"Mâgì",
                'episode': 1,
            },
            {
                'anime': u"Àccel wôrld",
                'episode': 1,
                'version': 2,
            },
        ]

        result = feeds.filter_episode_versions(episodes)
        self.assertEquals(sorted(result), sorted(expected))

    def test_filter_two_anime_three_episodes_one_version(self):
        episodes = [
            {
                'anime': u"Mâgì",
                'episode': 1,
            },
            {
                'anime': u"Àccel wôrld",
                'episode': 1,
                'version': 2,
            },
            {
                'anime': u"Àccel wôrld",
                'episode': 1,
            },
        ]
        expected = [
            {
                'anime': u"Mâgì",
                'episode': 1,
            },
            {
                'anime': u"Àccel wôrld",
                'episode': 1,
                'version': 2,
            },
        ]

        result = feeds.filter_episode_versions(episodes)
        self.assertEquals(sorted(result), sorted(expected))

    def test_filter_two_anime_four_episodes_four_versions(self):
        episodes = [
            {
                'anime': u"Àccel wôrld",
                'episode': 1,
                'version': 2,
            },
            {
                'anime': u"Mâgì",
                'episode': 1,
                'version': 1,
            },
            {
                'anime': u"Àccel wôrld",
                'episode': 1,
                'version': 1,
            },
            {
                'anime': u"Mâgì",
                'episode': 1,
                'version': 2,
            },
        ]
        expected = [
            {
                'anime': u"Mâgì",
                'episode': 1,
                'version': 2,
            },
            {
                'anime': u"Àccel wôrld",
                'episode': 1,
                'version': 2,
            },
        ]

        result = feeds.filter_episode_versions(episodes)
        self.assertEquals(sorted(result), sorted(expected))

    def test_filter_two_anime_four_episodes_two_versions(self):
        episodes = [
            {
                'anime': u"Àccel wôrld",
                'episode': 1,
                'version': 2,
            },
            {
                'anime': u"Mâgì",
                'episode': 1,
                'version': 2,
            },
            {
                'anime': u"Àccel wôrld",
                'episode': 1,
            },
            {
                'anime': u"Mâgì",
                'episode': 1,
            },
        ]
        expected = [
            {
                'anime': u"Mâgì",
                'episode': 1,
                'version': 2,
            },
            {
                'anime': u"Àccel wôrld",
                'episode': 1,
                'version': 2,
            },
        ]

        result = feeds.filter_episode_versions(episodes)
        self.assertEquals(sorted(result), sorted(expected))

    def test_filter_two_anime_six_episodes_four_versions(self):
        episodes = [
            {
                'anime': u"Mâgì",
                'episode': 1,
            },
            {
                'anime': u"Mâgì",
                'episode': 2,
                'version': 2,
            },
            {
                'anime': u"Mâgì",
                'episode': 2,
            },
            {
                'anime': u"Àccel wôrld",
                'episode': 2,
            },
            {
                'anime': u"Àccel wôrld",
                'episode': 1,
            },
            {
                'anime': u"Àccel wôrld",
                'episode': 2,
                'version': 2,
            },
        ]
        expected = [
            {
                'anime': u"Mâgì",
                'episode': 1,
            },
            {
                'anime': u"Mâgì",
                'episode': 2,
                'version': 2,
            },
            {
                'anime': u"Àccel wôrld",
                'episode': 1,
            },
            {
                'anime': u"Àccel wôrld",
                'episode': 2,
                'version': 2,
            },
        ]

        result = feeds.filter_episode_versions(episodes)
        self.assertEquals(sorted(result), sorted(expected))

class TestFetchEpisodesFromFeeds(unittest.TestCase):

    def setUp(self):
        self.nyaa_result = [{
            'subber'    : u'Commie',
            'anime'     : u'Sword Art Online',
            'episode'   : 2,
            'resolution': u'720p',
            'extension' : u'mkv',
        }]

    @patch('animesubs.feeds.fetch_episodes')
    def test_fetch_with_empty_config(self, mocked):
        config = {}
        expected = []
        mocked.return_value = []

        result = feeds.fetch_episodes_from_feeds(config)

        self.assertEquals(result, expected)
        self.assertFalse(mocked.called)

    @patch('animesubs.feeds.fetch_episodes')
    def test_fetch_one_feed(self, mocked):
        feedconfig = {'key': 'value'}
        feed = {'search': 'test'}
        config = {
            'feedtype': {
                'feedconfig': feedconfig,
                'feeds': [feed],
            }
        }

        mocked.return_value = self.nyaa_result

        result = feeds.fetch_episodes_from_feeds(config)

        mocked.assert_called_once_with('feedtype', feed, {'feedconfig':feedconfig})
        self.assertEquals(result, self.nyaa_result)

    @patch('animesubs.feeds.fetch_episodes')
    def test_fetch_one_feed(self, mocked):
        feedconfig = {'key': 'value'}
        feed = {'search': 'test'}
        config = {
            'feedtype': {
                'feedconfig': feedconfig,
                'feeds': [feed, feed],
            }
        }

        mocked.return_value = self.nyaa_result

        expected = self.nyaa_result * 2

        result = feeds.fetch_episodes_from_feeds(config)

        mocked.assert_called_with('feedtype', feed, {'feedconfig':feedconfig})
        self.assertEquals(result, expected)

if __name__ == "__main__":
    unittest.main()
