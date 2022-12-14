class Rating:
    def __init__(self, id_rater, id_rated, rating_text, rating_number):
        self._id_rater = id_rater
        self._id_rated = id_rated
        self._rating_text = rating_text
        self._rating_number = rating_number
        self._rater = None

    @property
    def id_rater(self):
        return self._id_rater

    @property
    def id_rated(self):
        return self._id_rated

    @property
    def rating_text(self):
        return self._rating_text

    @property
    def rating_number(self):
        return self._rating_number

    @property
    def rater(self):
        return self._rater

    @rater.setter
    def rater(self, rater):
        self._rater = rater

    @classmethod
    def init_rating_with_json(cls, json):
        return cls(json["id_rater"], json["id_rated"], json["rating_text"], json["rating_number"])

    def setRater(self, rater):
        self._rater = rater

    def convert_to_json(self):
        """
        Convert the current object into json
        :return: a json that represents the current object
        """
        json = {
            "id_rated": self._id_rated,
            "rating_text": self._rating_text,
            "rating_number": self._rating_number,
        }
        if self._rater is not None:
            json['rater'] = self._rater.convert_to_json(False)
        else:
            json['id_rater'] = self._id_rater
        return json
