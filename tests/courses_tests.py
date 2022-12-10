import unittest
from unittest.mock import Mock

import routes.courses
from data.CoursesDAO import CoursesDAO
from data.services.DALService import DALService


class CoursesTests(unittest.TestCase):
    def setUp(self):
        self.coursesDAO = CoursesDAO()

        self.dal_service = DALService()
        self.dal_service.start = Mock()
        self.course_from_db = [(1, 1, "Cours permettant de vous introduire le langage PHP. Aucun prérequis "
                                      "n'est nécessaire", 18.0, "Bruxelles", "Belgique", 1)]
        self.course_from_db_without_id_teacher = [
            (1, "Cours permettant de vous introduire le langage PHP. Aucun prérequis "
                "n'est nécessaire", 18.0, "Bruxelles", "Belgique", 1)]
        self.course_json = {
            "city": "Bruxelles",
            "country": "Belgique",
            "course_description": "Cours permettant de vous introduire le langage PHP. Aucun prérequis "
                                  "n'est nécessaire",
            "id_category": 1,
            "id_level": 1,
            "id_teacher": 1,
            "price_per_hour": 18.0
        }
        self.course_json_without_id_teacher = {
            "city": "Bruxelles",
            "country": "Belgique",
            "course_description": "Cours permettant de vous introduire le langage PHP. Aucun prérequis "
                                  "n'est nécessaire",
            "id_category": 1,
            "id_level": 1,
            "id_teacher": None,
            "price_per_hour": 18.0
        }

    def test_get_one_course_with_id_course_ok(self):
        self.dal_service.commit = Mock(return_value=self.course_from_db)
        response = routes.courses.get_one(1)
        self.assertEqual(200, response[1])
        self.assertEqual(self.course_json, response[0])

    def test_get_one_course_with_id_course_not_existing(self):
        self.dal_service.commit = Mock(return_value=[])
        try:
            routes.courses.get_one(100)
        except Exception as e:
            self.assertEqual(404, e.code)

    def test_get_one_course_with_id_course_lower_than_1(self):
        self.dal_service.commit = Mock(return_value=[])
        try:
            routes.courses.get_one(0)
        except Exception as e:
            self.assertEqual(400, e.code)

    def test_get_all_courses_from_teacher_id_ok(self):
        self.dal_service.commit = Mock(return_value=self.course_from_db_without_id_teacher)
        response = routes.courses.get_all_courses_from_teacher(1)
        self.assertEqual(200, response[1])
        self.assertEqual([self.course_json_without_id_teacher], response[0])

    def test_get_all_courses_from_teacher_id_lower_than_1(self):
        try:
            routes.courses.get_all_courses_from_teacher(0)
        except Exception as e:
            self.assertEqual(400, e.code)

    def test_get_all_courses_from_teacher_id_not_existing(self):
        self.dal_service.commit = Mock(return_value=[])
        try:
            routes.courses.get_all_courses_from_teacher(100)
        except Exception as e:
            self.assertEqual(404, e.code)


if __name__ == '__main__':
    unittest.main()
