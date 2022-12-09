import unittest
import requests
from requests import Response


class CoursesTests(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://localhost:5000/courses"
        self.course_1 = {
            "city": "Bruxelles",
            "country": "Belgique",
            "course_description": "Cours permettant de vous introduire le langage PHP. Aucun prérequis "
                                  "n'est nécessaire",
            "id_category": 1,
            "id_level": 1,
            "id_teacher": 1,
            "price_per_hour": 18.0
        }

    def test_get_one_course_with_id_course_ok(self):
        response = requests.get(f"{self.base_url}/1")
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.course_1, response.json())

    def test_get_one_course_with_id_course_not_existing(self):
        response = requests.get(f"{self.base_url}/8000")
        # If the test return true, that means course with id 8000 exists
        self.assertEqual(404, response.status_code)

    def test_get_one_course_with_id_course_lower_than_1(self):
        response = requests.get(f"{self.base_url}/0")
        self.assertEqual(400, response.status_code)


if __name__ == '__main__':
    unittest.main()
