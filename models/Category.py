class Category:

    def __init__(self, id_category, name):
        self._id_category = id_category
        self._name = name

    @property
    def id_category(self):
        return self._id_category

    @property
    def name(self):
        return self._name

    def convert_to_json(self):
        """
        Convert the current object into json
        :return: a json that represents the current object
        """
        return {
            "id_category": self.id_category,
            "name": self.name
        }
