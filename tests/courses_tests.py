import unittest
from unittest.mock import Mock
from flask import request
from app.main import app
from data.DAO.CoursesDAO import CoursesDAO
from data.services.DALService import DALService


class CoursesTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.coursesDAO = CoursesDAO()
        self.dal_service = DALService()
        self.dal_service.start = Mock()
        self.dal_service.commit_transaction = Mock()
        self.dal_service.rollback_transaction = Mock()
        self.course_from_db = [(3, "Cours d Anglais avec Browny", 25.0, "Bruxelles", "Belgique", "Débutant", 4,
                                "Anglais", 1, "Lambda", "Hugue", "Hugue@hugue", "hg", "male", "04", 0, 0)]
        self.course_from_teacher_from_db = [
            (3, "Cours d Anglais avec Browny", 25.0, "Bruxelles", "Belgique", "Débutant", 4,
             "Anglais", 1, "Lambda", "Hugue", "Hugue@hugue", "hg", "male", "04", 0, 0),
            (3, "Cours d Anglais avec Browny", 25.0, "Bruxelles", "Belgique", "Débutant", 4,
             "Anglais", 1, "Lambda", "Hugue", "Hugue@hugue", "hg", "male", "04", 0, 0)]
        self.course_json = {
            "category": {
                "id_category": 4,
                "name": "Anglais"
            },
            "city": "Bruxelles",
            "country": "Belgique",
            "course_description": "Cours d Anglais avec Browny",
            "id_course": 3,
            "level": "Débutant",
            "price_per_hour": 25.0,
            "sum_stars": 0,
            "teacher": {
                "email": "Hugue@hugue",
                "firstname": "Hugue",
                "id_user": 1,
                "lastname": "Lambda",
                "password": None,
                "phone": "04",
                "pseudo": "hg",
                "sexe": "male"
            },
            "total_tuples_stars": 0
        }
        self.courses_from_teacher_json = [
            {
                "category": {
                    "id_category": 4,
                    "name": "Anglais"
                },
                "city": "Bruxelles",
                "country": "Belgique",
                "course_description": "Cours d Anglais avec Browny",
                "id_course": 3,
                "level": "Débutant",
                "price_per_hour": 25.0,
                "sum_stars": 0,
                "teacher": {
                    "email": "Hugue@hugue",
                    "firstname": "Hugue",
                    "id_user": 1,
                    "lastname": "Lambda",
                    "password": None,
                    "phone": "04",
                    "pseudo": "hg",
                    "sexe": "male"
                },
                "total_tuples_stars": 0
            },
            {
                "category": {
                    "id_category": 4,
                    "name": "Anglais"
                },
                "city": "Bruxelles",
                "country": "Belgique",
                "course_description": "Cours d Anglais avec Browny",
                "id_course": 3,
                "level": "Débutant",
                "price_per_hour": 25.0,
                "sum_stars": 0,
                "teacher": {
                    "email": "Hugue@hugue",
                    "firstname": "Hugue",
                    "id_user": 1,
                    "lastname": "Lambda",
                    "password": None,
                    "phone": "04",
                    "pseudo": "hg",
                    "sexe": "male"
                },
                "total_tuples_stars": 0
            }
        ]

    def test_get_one_course_with_id_course_ok(self):
        self.dal_service.execute = Mock(return_value=self.course_from_db)
        response = self.app.get("courses/1")
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.course_json, response.get_json())

    def test_get_one_course_with_id_course_not_existing(self):
        self.dal_service.execute = Mock(return_value=[])
        response = self.app.get("courses/100")
        self.assertEqual(404, response.status_code)

    def test_get_one_course_with_id_course_lower_than_1(self):
        self.dal_service.execute = Mock(return_value=[])
        response = self.app.get("courses/0")
        self.assertEqual(400, response.status_code)

    # def test_get_all_courses_from_teacher_id_ok(self):
    #     self.dal_service.execute = Mock(return_value=self.course_from_teacher_from_db)
    #     response = self.app.get("courses/teacher")
    #     self.assertEqual(200, response.status_code)
    #     self.assertEqual(self.courses_from_teacher_json, response.get_json())

    def test_get_all_courses_from_teacher_without_token(self):
        response = self.app.get("courses/teacher")
        self.assertEqual(400, response.status_code)

    def test_get_all_courses_from_teacher_id_not_existing(self):
        self.dal_service.execute = Mock(return_value=[])
        response = self.app.get("courses/teacher/100")
        self.assertEqual(404, response.status_code)


if __name__ == '__main__':
    unittest.main()
