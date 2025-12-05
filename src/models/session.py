from collections import defaultdict
from .swipe import Swipe

class Session:
    def __init__(self):
        self.swipes = []
        self.country_likes = defaultdict(int)

    def record_swipe(self, artwork, direction):
        self.swipes.append(Swipe(artwork, direction))

        if direction == "like":
            country_name = artwork.country.name
            self.country_likes[country_name] += 1

    def get_top_countries(self):
        if not self.country_likes:
            return []

        # Find max likes
        max_likes = max(self.country_likes.values())

        # Get all countries with that number
        tied = [country for country, likes in self.country_likes.items()
                if likes == max_likes]

        return tied
