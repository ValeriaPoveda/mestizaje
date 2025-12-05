import unittest
import os

from src.controller.swipe_manager import SwipeManager
from src.loader.dataset_loader import DatasetLoader

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, "data", "dataset.json")


class TestSwipeManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        loader = DatasetLoader(DATASET_PATH)
        countries = loader.load()

        cls.manager = SwipeManager(countries, max_artworks=10)

    def test_initial_index_starts_at_zero(self):
        self.assertEqual(self.manager.index, 0)

    def test_artworks_loaded(self):
        self.assertGreater(len(self.manager.artworks), 0)
        self.assertLessEqual(len(self.manager.artworks), 10) 

    def test_get_current_artwork_returns_valid_artwork(self):
        art = self.manager.get_current_artwork()
        self.assertIsNotNone(art)
        self.assertTrue(hasattr(art, "id"))
        self.assertTrue(hasattr(art, "path"))

    def test_swipe_increments_index(self):
        start = self.manager.index
        self.manager.swipe("right")
        self.assertEqual(self.manager.index, start + 1)

    def test_swipe_records_session(self):
        self.manager.index = 0
        art = self.manager.get_current_artwork()
        self.manager.swipe("left")

        results = self.manager.session.swipes
        self.assertGreater(len(results), 0)

    def test_swipe_until_finished(self):
        self.manager.index = len(self.manager.artworks) - 1
        self.manager.swipe("right")
        self.assertTrue(self.manager.is_session_finished())

    def test_counter_outputs_two_integers(self):
        current, total = self.manager.get_counter()
        self.assertIsInstance(current, int)
        self.assertIsInstance(total, int)

    def test_counter_never_exceeds_total(self):
        current, total = self.manager.get_counter()
        self.assertLessEqual(current, total)


if __name__ == "__main__":
    unittest.main()
