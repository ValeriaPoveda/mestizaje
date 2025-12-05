import unittest
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATASET_PATH = os.path.join(BASE_DIR, "data", "dataset.json")
ARTWORKS_DIR = os.path.join(BASE_DIR, "artworks")
ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]


def _find_image(base_path):
    base, _ = os.path.splitext(base_path)
    filename = os.path.basename(base)
    directory = os.path.dirname(base)

    digits_only = "".join(ch for ch in filename if ch.isdigit())
    names = [filename]
    if digits_only and digits_only not in names:
        names.append(digits_only)

    directories = [directory]
    if directory.startswith("artworks"):
        tail = directory[len("artworks") + 1:] if len(directory) > len("artworks") else ""
        for batch in ("batch1", "batch2"):
            batch_dir = os.path.join("artworks", batch, tail) if tail else os.path.join("artworks", batch)
            directories.append(batch_dir)

    for name in names:
        for ext in ALLOWED_EXTENSIONS:
            for dir_path in directories:
                if os.path.isfile(os.path.join(dir_path, name + ext)):
                    return True
    return False


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
                    if not _find_image(path):
                        missing.append(path)

        self.assertEqual(
            len(missing), 0,
            f"Missing artwork files:\n" + "\n".join(missing[:20])
        )


if __name__ == "__main__":
    unittest.main()
