import unittest
from unittest.mock import Mock

from app.main import app
from data.DAO.CategoriesDAO import CategoriesDAO
from data.DAO.RatingsDAO import RatingsDAO
from data.DAO.UsersDAO import UsersDAO
from data.services.DALService import DALService


class RatingsTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.ratings_dao = RatingsDAO()
        self.users_dao = UsersDAO()
        self.dal_service = DALService()
        self.dal_service.start = Mock()
        self.dal_service.commit_transaction = Mock()
        self.dal_service.rollback_transaction = Mock()
        self.rating_json = {
            "id_rater": 1,
            "id_rated": -1,
            "rating_text": "bof comme prof j'ai pas vrmt apprécié",
            "rating_number": 3
        }
        self.correct_rating_json = {
            "id_rater": 1,
            "id_rated": 2,
            "rating_text": "bof comme prof j'ai pas vrmt apprécié",
            "rating_number": 3
        }
        self.all_appointments = [
            {
                "appointment_date": "2022-10-20",
                "appointment_state": "canceled",
                "box_house": "None",
                "id_course": 1,
                "id_student": 1,
                "number_house": 121,
                "street": "rue de la colline"
            }
        ]
        self.student = [(1, "Dupont","Pierre", "requinFR@gmail.com", "REQUIN", "male", "(+32)4 77 123 659", "motDePasse")]
        self.teacher = [(2, "Dupré", "Pedro", "Pedro@gmail.com", "Pedro", "male","(+32)4 77 444 659", "motDePasse2" )]

    def test_create_rating_negative_id_teacher(self):
        self.dal_service.execute = Mock()
        response = self.app.post('/ratings/', json=self.rating_json)
        self.assertEqual(400, response.status_code)

    def test_create_rating(self):
        self.dal_service.execute = Mock(side_effect=[self.student, self.teacher, self.all_appointments])
        #self.users_dao.get_user_by_id = Mock(return_value="user")
        response = self.app.post('/ratings/', json=self.correct_rating_json)

        self.assertEqual(201, response.status_code)


if __name__ == '__main__':
    unittest.main()
