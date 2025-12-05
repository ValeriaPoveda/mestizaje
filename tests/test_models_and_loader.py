import unittest
import os

from src.loader.dataset_loader import DatasetLoader

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, "data", "dataset.json")

class TestModelsAndLoader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.loader = DatasetLoader(DATASET_PATH)

        cls.countries = cls.loader.load()

        cls.artists = [artist for c in cls.countries for artist in c.artists]

        cls.artworks = [art for artist in cls.artists for art in artist.artworks]

    def test_loader_loads_countries(self):
        self.assertGreaterEqual(len(self.countries), 1)

    def test_loader_loads_artists(self):
        self.assertGreater(len(self.artists), 0)

    def test_loader_loads_artworks(self):
        self.assertGreater(len(self.artworks), 0)

    def test_country_model_fields(self):
        c = self.countries[0]
        self.assertTrue(hasattr(c, "id"))
        self.assertTrue(hasattr(c, "name"))
        self.assertTrue(hasattr(c, "artists"))

    def test_artist_model_fields(self):
        a = self.artists[0]
        self.assertTrue(hasattr(a, "id"))
        self.assertTrue(hasattr(a, "name"))
        self.assertTrue(hasattr(a, "country_id"))

    def test_artwork_model_fields(self):
        w = self.artworks[0]
        self.assertTrue(hasattr(w, "id"))
        self.assertTrue(hasattr(w, "path"))
        self.assertTrue(hasattr(w, "artist"))
        self.assertTrue(hasattr(w, "country"))

    def test_artists_link_to_valid_country(self):
        country_ids = {c.id for c in self.countries}
        for a in self.artists:
            self.assertIn(a.country_id, country_ids)

    def test_artworks_link_to_valid_artist(self):
        artist_ids = {a.id for a in self.artists}
        for w in self.artworks:
            self.assertIn(w.artist.id, artist_ids)

if __name__ == "__main__":
    unittest.main()
