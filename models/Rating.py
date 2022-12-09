class Rating:
    def __init__(self, id_rater, id_rated, rating_text, rating_number):
        self.id_rater = id_rater
        self.id_rated = id_rated
        self.rating_text = rating_text
        self.rating_number = rating_number

    @classmethod
    def init_rating_with_json(cls, json):
        return cls(json["id_rater"], json["id_rated"], json["rating_text"], json["rating_number"])

    def convert_to_json(self):
        return {
            "id_rater": self.id_rater,
            "id_rated": self.id_rated,
            "rating_text": self.rating_text,
            "rating_number": self.rating_number,
        }
