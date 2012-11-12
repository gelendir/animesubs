import unittest
from animesubs import lib


class TestFilenameWithSpaces(unittest.TestCase):

    def setUp(self):
        self.filename = "[Commie] Sword Art Online - 12v2 [ABCD1234].mkv"
        self.info = lib.info_from_filename(self.filename)

    def test_subber(self):
        self.assertEquals(self.info['subber'], 'Commie')

    def test_anime_name(self):
        self.assertEquals(self.info['anime'], "Sword Art Online")

    def test_anime_episode(self):
        self.assertEquals(self.info['episode'], 12)

    def test_episode_version(self):
        self.assertEquals(self.info['version'], 2)

    def test_extension(self):
        self.assertEquals(self.info['extension'], 'mkv')

class TestFilenameWithUnderscores(unittest.TestCase):

    def setUp(self):
        self.filename = "[Commie]_Sword_Art_Online_-_12v2_[ABCD1234].mkv"
        self.info = lib.info_from_filename(self.filename)

    def test_subber(self):
        self.assertEquals(self.info['subber'], 'Commie')

    def test_anime_name(self):
        self.assertEquals(self.info['anime'], "Sword Art Online")

    def test_anime_episode(self):
        self.assertEquals(self.info['episode'], 12)

    def test_episode_version(self):
        self.assertEquals(self.info['version'], 2)

    def test_extension(self):
        self.assertEquals(self.info['extension'], 'mkv')


class TestFilenameWithDashes(unittest.TestCase):

    def setUp(self):
        self.filename = "[UTW] Fate - Zero - 3 [ABCD1234].mkv"
        self.info = lib.info_from_filename(self.filename)

    def test_subber(self):
        self.assertEquals(self.info['subber'], 'UTW')

    def test_anime_name(self):
        self.assertEquals(self.info['anime'], 'Fate - Zero')

    def test_anime_episode(self):
        self.assertEquals(self.info['episode'], 3)

    def test_extension(self):
        self.assertEquals(self.info['extension'], 'mkv')


class TestFilenameWithOnlyResolution(unittest.TestCase):

    def setUp(self):
        self.filename = "[HorribleSubs] Magi - 04 [1080p].mkv"
        self.info = lib.info_from_filename(self.filename)

    def test_subber(self):
        self.assertEquals(self.info['subber'], 'HorribleSubs')

    def test_anime_name(self):
        self.assertEquals(self.info['anime'], 'Magi')

    def test_anime_episode(self):
        self.assertEquals(self.info['episode'], 4)

    def test_resolution(self):
        self.assertEquals(self.info['resolution'], '1080p')

    def test_extension(self):
        self.assertEquals(self.info['extension'], 'mkv')

class TestFilenameWithAdditionalInfo(unittest.TestCase):

    def setUp(self):
        self.filename = "[UTW-Mazui]_Kill_Me_Baby_-_07_[BD][h264-720p][3E82FF36].mkv"
        self.info = lib.info_from_filename(self.filename)

    def test_subber(self):
        self.assertEquals(self.info['subber'], 'UTW-Mazui')

    def test_anime_name(self):
        self.assertEquals(self.info['anime'], 'Kill Me Baby')

    def test_anime_episode(self):
        self.assertEquals(self.info['episode'], 7)

    def test_resolution(self):
        self.assertEquals(self.info['resolution'], '720p')

    def test_extension(self):
        self.assertEquals(self.info['extension'], 'mkv')

    def test_crc32(self):
        self.assertEquals(self.info['crc32'], '3E82FF36')

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

