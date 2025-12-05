class Artist:
    def __init__(self, artist_id, name, country):
        self.id = artist_id
        self.name = name
        self.country = country
        self.country_id = country.id
        self.artworks = []

    def add_artwork(self, artwork):
        self.artworks.append(artwork)
