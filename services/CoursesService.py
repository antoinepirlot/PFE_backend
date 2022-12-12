from Exceptions.FatalException import FatalException
from Exceptions.WebExceptions.NotFoundException import NotFoundException
from data.DAO.CoursesDAO import CoursesDAO
from data.services.DALService import DALService
from utils.objects_modifications import convert_models_objects_to_json


class CoursesService:
    _courses_dao = CoursesDAO()
    _dal_service = DALService()

    def __init__(self):
        pass

    def get_one(self, id_course):
        try:
            self._dal_service.start()
            course = self._courses_dao.get_one(id_course)
            if course is None:
                raise NotFoundException(f"No course matching id: {id_course}")
            self._dal_service.commit_transaction()
            return course.convert_to_json()
        except FatalException as e:
            self._dal_service.rollback_transaction()
            raise e

    def get_all_courses(self):
        try:
            self._dal_service.start()
            courses = self._courses_dao.get_all_courses()
            if courses is None:
                raise NotFoundException
            self._dal_service.commit_transaction()
            return courses
        except FatalException as e:
            self._dal_service.rollback_transaction()
            raise e

    def get_all_courses_from_teacher(self, id_teacher):
        """
        Get courses from DAO and convert them to json
        :param id_teacher: the teacher's id matching with courses
        :return: the list of converted courses in json matching the teacher's id
        """
        try:
            self._dal_service.start()
            courses = self._courses_dao.get_all_courses_from_teacher(id_teacher)
            if courses is None:
                raise NotFoundException
            self._dal_service.commit_transaction()
            return convert_models_objects_to_json(courses)
        except FatalException as e:
            self._dal_service.rollback_transaction()
            raise e

    def create_one_course(self, course):
        try:
            self._dal_service.start()
            result = self._courses_dao.create_one_course(course)
            self._dal_service.commit_transaction()
            return result
        except FatalException as e:
            self._dal_service.rollback_transaction()
            raise e
