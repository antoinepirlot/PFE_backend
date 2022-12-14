from Exceptions.WebExceptions.NotFoundException import NotFoundException
from data.DAO.CategoriesDAO import CategoriesDAO
from data.DAO.CoursesDAO import CoursesDAO
from data.DAO.SkillsDAO import SkillsDAO
from data.DAO.UsersDAO import UsersDAO
from data.services.DALService import DALService
from models.Skill import Skill
from utils.objects_modifications import convert_models_objects_to_json


class CoursesService:


    def __init__(self):
        pass

    def __new__(cls):
        if not hasattr(cls, "_instance"):
            # No instance of CoursesService class, a new one is created
            cls._dal_service = DALService()
            cls._courses_dao = CoursesDAO()
            cls._users_dao = UsersDAO()
            cls._categories_dao = CategoriesDAO()
            cls._skills_dao = SkillsDAO()
            cls._instance = super(CoursesService, cls).__new__(cls)
        # There's already an instance of CoursesService class, so the existing one is returned
        return cls._instance


    def get_one(self, id_course):
        """
        Get one course retrieved by its id
        :param id_course: the id of the course
        :return: the course with the good id or Not found
        """
        try:
            self._dal_service.start()
            course = self._courses_dao.get_one(id_course)
            if course is None:
                raise NotFoundException(f"No course matching id: {id_course}")
            self._dal_service.commit_transaction()
            return course.convert_to_json()
        except Exception as e:
            self._dal_service.rollback_transaction()
            raise e

    def get_all_courses(self, filter=None):
        """
        Get all courses with a filter or not
        :param filter: by what you want to filter all courses
        :return: all courses with the potential filter applied
        """
        try:
            self._dal_service.start()
            courses = self._courses_dao.get_all_courses(filter)
            if courses is None:
                raise NotFoundException
            self._dal_service.commit_transaction()
            return courses
        except Exception as e:
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
            return courses
        except Exception as e:
            self._dal_service.rollback_transaction()
            raise e

    def create_one_course(self, course):
        """
        create one course
        :param course: the course we want to create
        :return: the created course
        """
        try:
            self._dal_service.start()

            ##check if teacher got the skill, if not add it
            user = self._users_dao.get_user_by_id(course.id_teacher)
            if user is None:
                raise NotFoundException("User not found")
            all_skills = self._categories_dao.get_all_skills_categories(course.id_teacher)
            user.skills = all_skills
            bool = False
            for s in all_skills:
                if s.id_category == course.id_category:
                    bool = True

            if not bool:  # if false we add the skill to the teacher
                skill = Skill(course.id_category, course.id_teacher)
                self._skills_dao.add_skill(skill)

            result = self._courses_dao.create_one_course(course)
            self._dal_service.commit_transaction()
            return result
        except Exception as e:
            self._dal_service.rollback_transaction()
            raise e
