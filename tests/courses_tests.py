import unittest
from unittest.mock import Mock

from app.main import app
from data.CoursesDAO import CoursesDAO
from data.services.DALService import DALService


class CoursesTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.coursesDAO = CoursesDAO()
        self.dal_service = DALService()
        self.dal_service.start = Mock()
        self.dal_service.commit_transaction = Mock()
        self.dal_service.rollback_transaction = Mock()
        self.course_from_db = [(1, 1, "Cours permettant de vous introduire le langage PHP. Aucun prérequis "
                                      "n'est nécessaire", 18.0, "Bruxelles", "Belgique", "Débutant")]
        self.course_from_db_without_id_teacher = [
            (1, "Cours permettant de vous introduire le langage PHP. Aucun prérequis "
                "n'est nécessaire", 18.0, "Bruxelles", "Belgique", "Débutant")]
        self.course_json = {
            "city": "Bruxelles",
            "country": "Belgique",
            "course_description": "Cours permettant de vous introduire le langage PHP. Aucun prérequis "
                                  "n'est nécessaire",
            "id_category": 1,
            "level": "Débutant",
            "id_teacher": 1,
            "price_per_hour": 18.0
        }
        self.course_json_without_id_teacher = {
            "city": "Bruxelles",
            "country": "Belgique",
            "course_description": "Cours permettant de vous introduire le langage PHP. Aucun prérequis "
                                  "n'est nécessaire",
            "id_category": 1,
            "level": "Débutant",
            "id_teacher": None,
            "price_per_hour": 18.0
        }

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

    def test_get_all_courses_from_teacher_id_ok(self):
        self.dal_service.execute = Mock(return_value=self.course_from_db_without_id_teacher)
        response = self.app.get("courses/teacher/1")
        self.assertEqual(200, response.status_code)
        self.assertEqual([self.course_json_without_id_teacher], response.get_json())

    def test_get_all_courses_from_teacher_id_lower_than_1(self):
        response = self.app.get("courses/teacher/0")
        self.assertEqual(400, response.status_code)

    def test_get_all_courses_from_teacher_id_not_existing(self):
        self.dal_service.execute = Mock(return_value=[])
        response = self.app.get("courses/teacher/100")
        self.assertEqual(404, response.status_code)


if __name__ == '__main__':
    unittest.main()
