import unittest
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATASET_PATH = os.path.join(BASE_DIR, "data", "dataset.json")
ARTWORKS_DIR = os.path.join(BASE_DIR, "artworks")
ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]


class TestDatasetAndPaths(unittest.TestCase):

    def setUp(self):
        with open(DATASET_PATH, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def test_dataset_loads(self):
        self.assertIsInstance(self.data, dict)

    def test_country_count(self):
        self.assertEqual(len(self.data["countries"]), 33)

    def test_countries_have_required_fields(self):
        for country in self.data["countries"]:
            self.assertIn("code", country)
            self.assertIn("name", country)
            self.assertIn("artists", country)

    def test_artists_have_required_fields(self):
        for country in self.data["countries"]:
            for artist in country["artists"]:
                self.assertIn("id", artist)
                self.assertIn("name", artist)
                self.assertIn("artworks", artist)

    def test_artworks_have_required_fields(self):
        for country in self.data["countries"]:
            for artist in country["artists"]:
                for art in artist["artworks"]:
                    self.assertIn("id", art)
                    self.assertIn("path", art)
                    
    def test_artwork_files_exist(self):
        """Ensure that every file listed in the dataset exists in /artworks (with common extensions)"""
        missing = []

        for country in self.data["countries"]:
            for artist in country["artists"]:
                for art in artist["artworks"]:
                    path = art["path"]
                    base, _ = os.path.splitext(path)
                    filename = os.path.basename(base)
                    directory = os.path.dirname(base)
                    digits_only = "".join(ch for ch in filename if ch.isdigit())

                    name_candidates = [filename]
                    if digits_only and digits_only not in name_candidates:
                        name_candidates.append(digits_only)

                    exists = False
                    for name in name_candidates:
                        for ext in ALLOWED_EXTENSIONS:
                            candidate = os.path.join(directory, name + ext)
                            if os.path.isfile(candidate):
                                exists = True
                                break
                        if exists:
                            break

                    if not exists:
                        missing.append(path)

        self.assertEqual(
            len(missing), 0,
            f"Missing artwork files:\n" + "\n".join(missing[:20])
        )


if __name__ == "__main__":
    unittest.main()
