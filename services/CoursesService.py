from data.CoursesDAO import CoursesDAO
from data.services.DALService import DALService
from utils.objects_modifications import convert_models_objects_to_json


class CoursesService:
    _courses_dao = CoursesDAO()
    _dal_service = DALService()

    def __init__(self):
        pass

    def get_one(self, id_course):
        self._dal_service.start()
        course = self._courses_dao.get_one(id_course)
        if course is None:
            self._dal_service.rollback_transaction()
            return None
        self._dal_service.commit_transaction()
        return course.convert_to_json()

    def get_all_courses_from_teacher(self, id_teacher):
        """
        Get courses from DAO and convert them to json
        :param id_teacher: the teacher's id matching with courses
        :return: the list of converted courses in json matching the teacher's id
        """
        courses = None
        try:
            self._dal_service.start()
            courses = self._courses_dao.get_all_courses_from_teacher(id_teacher)
            self._dal_service.commit_transaction()
        except Exception as sql_error:  # TODO maybe psycopg2.Error
            self._dal_service.rollback_transaction()
        if courses is not None:
            return convert_models_objects_to_json(courses)
        return None

    def create_one_course(self, course):
        try:
            self._dal_service.start()
            result = self._courses_dao.create_one_course(course)
            self._dal_service.commit_transaction()
            return result
        except Exception as e:
            self._dal_service.rollback_transaction()
