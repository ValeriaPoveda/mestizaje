class Artwork:
    def __init__(self, artwork_id, path, artist, country):
        self.id = artwork_id
        self.artwork_id = artwork_id  # backward compatibility
        self.path = path
        self.artist = artist
        self.country = country
