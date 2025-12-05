import random
from src.models.session import Session

class SwipeManager:

    def __init__(self, countries, max_artworks=40):
        self.countries = countries
        self.max_artworks = max_artworks
        self.session = Session()

        # Flatten all artworks
        all_artworks = self._flatten_artworks()

        if not all_artworks:
            raise ValueError("No artworks available to display.")

        # Pick 40 unique ones
        self.artworks = random.sample(all_artworks, min(max_artworks, len(all_artworks)))

        self.index = 0

    def _flatten_artworks(self):
        flat = []
        for country in self.countries:
            for artist in country.artists:
                for art in artist.artworks:
                    flat.append(art)
        return flat

    def start_session(self):
        self.index = 0
        self.session = Session()

    def get_current_artwork(self):
        if self.index < len(self.artworks):
            return self.artworks[self.index]
        return None

    def swipe(self, direction):
        """
        Compatibility wrapper used in tests.
        Accepts 'right'/'left' and maps to like/skip.
        """
        mapped = direction
        if direction == "right":
            mapped = "like"
        elif direction == "left":
            mapped = "skip"
        self.handle_choice(mapped)

    def handle_choice(self, direction):
        artwork = self.get_current_artwork()
        if artwork:
            self.session.record_swipe(artwork, direction)
            self.index += 1

    def is_session_finished(self):
        return self.index >= len(self.artworks)

    def get_results(self):
        return self.session.get_top_countries()

    def get_counter(self):
        # Returns like: (currentNumber, total)
        total = len(self.artworks)
        current = min(self.index + 1, total) if total else 0
        return (current, total)
