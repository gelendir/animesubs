import unittest
from animesubs import lib


class TestInfoFromFilenameWithSpaces(unittest.TestCase):

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


class TestInfoFilenameWithUnderscores(unittest.TestCase):

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


if __name__ == "__main__":
    unittest.main()

