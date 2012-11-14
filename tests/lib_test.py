# coding=utf8
import unittest
from animesubs import lib


class TestInfoFromFilename(unittest.TestCase):

    def test_filename_with_spaces(self):
        filename = "[Commie] Sword Art Online - 12v2 [ABCD1234].mkv"
        expected = {
            'subber'    : u'Commie',
            'anime'     : u'Sword Art Online',
            'episode'   : 12,
            'version'   : 2,
            'crc32'     : 'ABCD1234',
            'extension' : u'mkv',
        }

        result = lib.info_from_filename(filename)
        self.assertEquals(expected, result)

    def test_filename_with_underscores(self):
        filename = "[Commie]_Sword_Art_Online_-_12v2_[ABCD1234].mkv"
        expected = {
            'subber'    : u'Commie',
            'anime'     : u'Sword Art Online',
            'episode'   : 12,
            'version'   : 2,
            'crc32'     : u'ABCD1234',
            'extension' : u'mkv',
        }

        result = lib.info_from_filename(filename)
        self.assertEquals(expected, result)

    def test_filename_with_unicode(self):
        filename = u"[Whatup] 「CØDE：BREAKER」_-_34_[720p][10bit][1234ABCD].mkv"
        expected = {
            'subber'     : u'Whatup',
            'anime'      : u'「CØDE：BREAKER」',
            'episode'    : 34,
            'resolution' : u'720p',
            'crc32'      : u'1234ABCD',
            'extension'  : u'mkv',
        }

        result = lib.info_from_filename(filename)
        self.assertEquals(expected, result)

    def test_filename_with_dashes(self):
        filename = "[UTW] Fate - Zero - 3 [ABCD1234].mkv"
        expected = {
            'subber'     : u'UTW',
            'anime'      : u'Fate - Zero',
            'episode'    : 3,
            'crc32'      : u'ABCD1234',
            'extension'  : u'mkv',
        }

        result = lib.info_from_filename(filename)
        self.assertEquals(expected, result)

    def test_filename_with_only_resolution(self):
        filename = "[HorribleSubs] Magi - 04 [1080p].mkv"
        expected = {
            'subber'     : u'HorribleSubs',
            'anime'      : u'Magi',
            'episode'    : 4,
            'resolution' : '1080p',
            'extension'  : u'mkv',
        }

        result = lib.info_from_filename(filename)
        self.assertEquals(expected, result)

    def test_filename_with_additional_info(self):
        filename = "[UTW-Mazui]_Kill_Me_Baby_-_07_[BD][h264-720p][3E82FF36].mkv"
        expected = {
            'subber'     : u'UTW-Mazui',
            'anime'      : u'Kill Me Baby',
            'episode'    : 7,
            'resolution' : '720p',
            'crc32'      : '3E82FF36',
            'extension'  : u'mkv',
        }

        result = lib.info_from_filename(filename)
        self.assertEquals(expected, result)

class TestFilterExisting(unittest.TestCase):

    def test_empty_filelist(self):
        episodes = []
        filelist = []
        result = lib.filter_existing(filelist, episodes)
        self.assertEquals(result, [])

    def test_one_episode_no_files(self):
        episodes = [
            {'filename': "[HorribleSubs] Magi - 04 [1080p].mkv"}
        ]
        filelist = []
        result = lib.filter_existing(filelist, episodes)
        self.assertEquals(result, [])

    def test_one_file_no_episodes(self):
        episodes = []
        filelist = [
            "[HorribleSubs] Magi - 04 [1080p].mkv"
        ]
        result = lib.filter_existing(filelist, episodes)
        self.assertEquals(result, [])

    def test_filename_with_underscores(self):
        episodes = [
            {'filename': "[HorribleSubs] Magi - 04 [1080p].mkv"}
        ]
        filelist = [
            "[HorribleSubs]_Magi_-_04_[1080p].mkv"
        ]
        result = lib.filter_existing(filelist, episodes)
        self.assertEquals(result, episodes)

    def test_random_files_in_filelist(self):
        episodes = [
            {'filename': "[HorribleSubs] Magi - 04 [1080p].mkv"}
        ]
        filelist = [
            "[HorribleSubs]_Magi_-_04_[1080p].mkv",
            "file1.txt",
            "file2.txt",
        ]
        result = lib.filter_existing(filelist, episodes)
        self.assertEquals(result, episodes)


    def test_two_episodes_one_file(self):
        episodes = [
            {'filename': "[HorribleSubs] Magi - 04 [1080p].mkv"},
            {'filename': "[HorribleSubs] Magi - 05 [1080p].mkv"},
        ]
        filelist = [
            "[HorribleSubs]_Magi_-_04_[1080p].mkv"
        ]

        expected = [
            {'filename': "[HorribleSubs] Magi - 04 [1080p].mkv"},
        ]

        result = lib.filter_existing(filelist, episodes)
        self.assertEquals(result, expected)

class TestFindMissingEpisodes(unittest.TestCase):

    def test_empty_filelist(self):
        filelist = []
        episodes = []
        result = lib.filter_missing(filelist, episodes)
        self.assertEquals(result, [])

    def test_one_episode_no_files(self):
        episodes = [
            {'filename': "[HorribleSubs] Magi - 04 [1080p].mkv"}
        ]
        filelist = []
        result = lib.filter_missing(filelist, episodes)
        self.assertEquals(result, episodes)

    def test_one_file_no_episodes(self):
        episodes = []
        filelist = [
            "[HorribleSubs] Magi - 04 [1080p].mkv"
        ]
        result = lib.filter_missing(filelist, episodes)
        self.assertEquals(result, [])

    def test_filename_with_underscores(self):
        episodes = [
            {'filename': "[HorribleSubs] Magi - 04 [1080p].mkv"}
        ]
        filelist = [
            "[HorribleSubs]_Magi_-_04_[1080p].mkv"
        ]
        result = lib.filter_missing(filelist, episodes)
        self.assertEquals(result, [])

    def test_random_files_in_filelist(self):
        episodes = [
            {'filename': "[HorribleSubs] Magi - 04 [1080p].mkv"}
        ]
        filelist = [
            "[HorribleSubs]_Magi_-_04_[1080p].mkv",
            "file1.txt",
            "file2.txt",
        ]
        result = lib.filter_missing(filelist, episodes)
        self.assertEquals(result, [])


    def test_two_episodes_one_file(self):
        episodes = [
            {'filename': "[HorribleSubs] Magi - 04 [1080p].mkv"},
            {'filename': "[HorribleSubs] Magi - 05 [1080p].mkv"},
        ]
        filelist = [
            "[HorribleSubs]_Magi_-_04_[1080p].mkv"
        ]

        expected = [
            {'filename': "[HorribleSubs] Magi - 05 [1080p].mkv"},
        ]

        result = lib.filter_missing(filelist, episodes)
        self.assertEquals(result, expected)


if __name__ == "__main__":
    unittest.main()

