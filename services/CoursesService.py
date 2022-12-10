from data.CoursesDAO import CoursesDAO
from utils.objects_modifications import convert_models_objects_to_json


class CoursesService:
    coursesDAO = CoursesDAO()

    def __init__(self):
        pass

    def get_one(self, id_course):
        course = self.coursesDAO.get_one(id_course)
        if course is not None:
            return course.convert_to_json()
        return None

    def get_all_courses_from_teacher(self, id_teacher):
        """
        Get courses from DAO and convert them to json
        :param id_teacher: the teacher's id matching with courses
        :return: the list of converted courses in json matching the teacher's id
        """
        courses = self.coursesDAO.get_all_courses_from_teacher(id_teacher)
        if courses is not None:
            return convert_models_objects_to_json(courses)
        return None

    def create_one_course(self, course):
        return self.coursesDAO.create_one_course(course)
