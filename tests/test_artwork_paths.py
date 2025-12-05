import unittest
import os
from src.loader.dataset_loader import DatasetLoader


ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]
DATASET_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "dataset.json")


class TestImagePaths(unittest.TestCase):

    def test_artwork_paths_exist(self):
        loader = DatasetLoader(DATASET_PATH)
        countries = loader.load()

        missing = []

        for country in countries:
            for artist in country.artists:
                for art in artist.artworks:
                    base, _ = os.path.splitext(art.path)
                    filename = os.path.basename(base)
                    directory = os.path.dirname(base)

                    # Try the declared filename and a digits-only fallback (e.g., AG01 -> 01)
                    digits_only = "".join(ch for ch in filename if ch.isdigit())
                    name_candidates = [filename]
                    if digits_only and digits_only not in name_candidates:
                        name_candidates.append(digits_only)

                    found = False
                    tried = []
                    for name in name_candidates:
                        for ext in ALLOWED_EXTENSIONS:
                            candidate = os.path.join(directory, name + ext)
                            tried.append(candidate)
                            if os.path.exists(candidate):
                                found = True
                                break
                        if found:
                            break

                    if not found:
                        missing.append((art.path, tried))

        if missing:
            print("\nMissing artwork files:")
            for original, attempts in missing[:10]:
                print(f"{original} -> tried: {attempts}")

        self.assertEqual(len(missing), 0, "Some artwork paths do NOT exist.")
