class Country:
    def __init__(self, country_id, name):
        # Store both id and code for compatibility with dataset/tests
        self.id = country_id
        self.code = country_id
        self.name = name
        self.artists = []
        self.score = 0  # runtime score

    def add_artist(self, artist):
        self.artists.append(artist)

    def add_score(self, increment=1):
        self.score += increment
