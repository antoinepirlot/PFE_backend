class Category:

    def __init__(self, id_category, name):
        self.id_category = id_category
        self.name = name

    def convert_to_json(self):
        """
        Convert the current object into json
        :return: a json that represents the current object
        """
        return {
            "id_category": self.id_category,
            "name": self.name
        }