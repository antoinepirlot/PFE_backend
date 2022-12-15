import unittest
from unittest.mock import Mock

from app.main import app
from data.DAO.RatingsDAO import RatingsDAO
from data.DAO.UsersDAO import UsersDAO
from data.services.DALService import DALService
from tests.utils_for_tests import get_good_token


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
        self.correct_rating_from_db = [(1, 2, "bof comme prof j'ai pas vrmt apprécié", 3)]
        self.empty_list = []
        self.all_appointments = [(1, 1, "finished", "2022-10-20", "rue de la colline", 121, None)]
        self.student = [(1, "Dupont", "Pierre", "requinFR@gmail.com", "REQUIN", "male", "(+32)4 77 123 659",
                         "motDePasse")]
        self.student_json = {'email': 'requinFR@gmail.com',
                             'firstname': 'Pierre',
                             'id_user': 1,
                             'lastname': 'Dupont',
                             'phone': '(+32)4 77 123 659',
                             'pseudo': 'REQUIN',
                             'sexe': 'male'}
        self.teacher = [(2, "Dupré", "Pedro", "Pedro@gmail.com", "Pedro", "male", "(+32)4 77 444 659", "motDePasse2")]

    def test_create_rating_all_good(self):
        self.dal_service.execute = Mock(side_effect=[self.student,
                                                     self.student,
                                                     self.teacher,
                                                     self.all_appointments,
                                                     self.empty_list,
                                                     None,
                                                     self.student,
                                                     None])

        token = get_good_token(1)
        response = self.app.post('/ratings/', json=self.correct_rating_json, headers={"Authorization": token})
        self.assertEqual(201, response.status_code)

    def test_get_ratings_from_teacher_success(self):
        correct_rating_json_with_rater = [{
            "rater": self.student_json,
            "id_rated": 2,
            "rating_text": "bof comme prof j'ai pas vrmt apprécié",
            "rating_number": 3
        }]
        self.dal_service.execute = Mock(side_effect=[self.teacher, self.correct_rating_from_db, self.student])
        response = self.app.get('/ratings/', query_string={'id_teacher': 2})
        self.assertEqual(200, response.status_code)
        self.assertEqual(correct_rating_json_with_rater, response.get_json())


if __name__ == '__main__':
    unittest.main()
