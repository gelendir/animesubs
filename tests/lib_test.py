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


if __name__ == "__main__":
    unittest.main()

