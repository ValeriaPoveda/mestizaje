import json
import os

from src.models.factories import CountryFactory, ArtistFactory, ArtworkFactory

ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]


class DatasetLoader:
    """
    Loads the JSON dataset and uses Factory Method classes
    to create Country, Artist, and Artwork objects.
    """

    def __init__(self, json_path):
        self.json_path = json_path

    def _resolve_artwork_path(self, path):
        """
        Return an existing image path if found (handles extension and digit-only fallbacks),
        otherwise None.
        """
        base, _ = os.path.splitext(path)
        filename = os.path.basename(base)
        directory = os.path.dirname(base)

        digits_only = "".join(ch for ch in filename if ch.isdigit())
        name_candidates = [filename]
        if digits_only and digits_only not in name_candidates:
            name_candidates.append(digits_only)

        for name in name_candidates:
            for ext in ALLOWED_EXTENSIONS:
                candidate = os.path.join(directory, name + ext)
                if os.path.exists(candidate):
                    return candidate
        return None

    def load(self):

        if not os.path.exists(self.json_path):
            raise FileNotFoundError(f"Dataset file missing: {self.json_path}")

        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        country_list = data.get("countries", [])

        countries = []

        for country_block in country_list:

            country_obj = CountryFactory.create(
                country_id=country_block.get("id", country_block.get("code")),
                name=country_block["name"]
            )

            has_artists = False
            for artist_block in country_block["artists"]:

                artist_obj = ArtistFactory.create(
                    artist_id=artist_block["id"],
                    name=artist_block["name"],
                    country=country_obj
                )

                for artwork_block in artist_block["artworks"]:

                    resolved_path = self._resolve_artwork_path(artwork_block["path"])
                    if not resolved_path:
                        # Skip missing images entirely
                        continue

                    artwork_obj = ArtworkFactory.create(
                        artwork_id=artwork_block["id"],
                        path=resolved_path,
                        artist=artist_obj,
                        country=country_obj
                    )

                    artist_obj.add_artwork(artwork_obj)

                if artist_obj.artworks:
                    country_obj.add_artist(artist_obj)
                    has_artists = True

            if has_artists:
                countries.append(country_obj)

        return countries
