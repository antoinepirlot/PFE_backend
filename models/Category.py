class Category:

    def __init__(self, id_category, name, color=None):
        self.id_category = id_category
        self.name = name
        self.color = color

    def convert_to_json(self):
        return {
            "id_category": self.id_category,
            "name": self.name
        }