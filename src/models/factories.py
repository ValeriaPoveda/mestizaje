from .country import Country
from .artist import Artist
from .artwork import Artwork


class CountryFactory:
    """Factory Method: Creates Country objects."""

    @staticmethod
    def create(country_id, name):
        return Country(country_id, name)


class ArtistFactory:
    """Factory Method: Creates Artist objects."""

    @staticmethod
    def create(artist_id, name, country):
        return Artist(artist_id, name, country)


class ArtworkFactory:
    """Factory Method: Creates Artwork objects."""

    @staticmethod
    def create(artwork_id, path, artist, country):
        return Artwork(artwork_id, path, artist, country)
