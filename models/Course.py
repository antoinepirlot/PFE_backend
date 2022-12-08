class Course:
    def __init__(self, id_category, id_teacher, course_description, price_per_hour, city, country, id_level):
        self.id_category = id_category
        self.id_teacher = id_teacher
        self.course_description = course_description
        self.price_per_hour = price_per_hour
        self.city = city
        self.country = country
        self.id_level = id_level

    def convert_to_json(self):
        return {"id_category": self.id_category,
                "id_teacher": self.id_teacher,
                "course_description": self.course_description,
                "price_per_hour": self.price_per_hour,
                "city": self.city,
                "country": self.country,
                "id_level": self.id_level
                }
