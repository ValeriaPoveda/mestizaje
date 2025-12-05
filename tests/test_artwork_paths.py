import unittest
import os
from src.loader.dataset_loader import DatasetLoader


ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]
DATASET_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "dataset.json")


def _find_image(base_path):
    """
    Returns True if any matching file exists in original directory or batch subdirectories.
    """
    base, _ = os.path.splitext(base_path)
    filename = os.path.basename(base)
    directory = os.path.dirname(base)

    # Try declared name and digits-only variant
    digits_only = "".join(ch for ch in filename if ch.isdigit())
    names = [filename]
    if digits_only and digits_only not in names:
        names.append(digits_only)

    # Directories to search
    directories = [directory]
    if directory.startswith("artworks"):
        tail = directory[len("artworks") + 1:] if len(directory) > len("artworks") else ""
        for batch in ("batch1", "batch2"):
            batch_dir = os.path.join("artworks", batch, tail) if tail else os.path.join("artworks", batch)
            directories.append(batch_dir)

    for name in names:
        for ext in ALLOWED_EXTENSIONS:
            for dir_path in directories:
                if os.path.exists(os.path.join(dir_path, name + ext)):
                    return True
    return False


class TestImagePaths(unittest.TestCase):

    def test_artwork_paths_exist(self):
        loader = DatasetLoader(DATASET_PATH)
        countries = loader.load()

        missing = []

        for country in countries:
            for artist in country.artists:
                for art in artist.artworks:
                    found = _find_image(art.path)
                    if not found:
                        missing.append(art.path)

        if missing:
            print("\nMissing artwork files:")
            for original in missing[:10]:
                print(original)

        self.assertEqual(len(missing), 0, "Some artwork paths do NOT exist.")
