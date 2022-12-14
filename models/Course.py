from models.Category import Category
from models.User import User


class Course(object):

    def __init__(self, id_category, id_teacher, course_description, price_per_hour, city, country, level,
                 sum_stars=None, total_tuples_stars=None):
        self._id_course = None
        self._id_category = id_category
        self._id_teacher = id_teacher
        self._course_description = course_description
        self._price_per_hour = price_per_hour
        self._city = city
        self._country = country
        self._level = level
        self._sum_stars = sum_stars
        self._total_tuples_stars = total_tuples_stars

    @property
    def id_course(self):
        return self._id_course

    @id_course.setter
    def id_course(self, id_course):
        self._id_course = id_course

    @property
    def id_category(self):
        return self._id_category

    @property
    def id_teacher(self):
        return self._id_teacher

    @property
    def course_description(self):
        return self._course_description

    @property
    def price_per_hour(self):
        return self._price_per_hour

    @property
    def city(self):
        return self._city

    @property
    def country(self):
        return self._country

    @property
    def level(self):
        return self._level

    @property
    def sum_stars(self):
        return self._sum_stars

    @property
    def total_tuples_stars(self):
        return self._total_tuples_stars

    def convert_to_json(self):
        """
        Convert the current object into json
        :return: a json that represents the current object
        """
        json = {"course_description": self._course_description,
                "price_per_hour": self._price_per_hour,
                "city": self._city,
                "country": self._country,
                "level": self._level,
                "sum_stars": self._sum_stars,
                "total_tuples_stars": self._total_tuples_stars
                }
        if type(self._id_teacher) is User:
            json["teacher"] = self._id_teacher.convert_to_json()
        else:
            json["id_teacher"] = self._id_teacher
        if type(self._id_category) is Category:
            json["category"] = self._id_category.convert_to_json()
        else:
            json["id_category"] = self._id_category
        if self._id_course is not None:
            json["id_course"] = self._id_course
        return json
