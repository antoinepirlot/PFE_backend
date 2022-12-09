from data.CoursesDAO import CoursesDAO


class CoursesService:
    coursesDAO = CoursesDAO()

    def __init__(self):
        pass

    def get_one(self, id_course):
        course = self.coursesDAO.get_one(id_course)
        if course is not None:
            return course.convert_to_json()
        return None

    def create_one_course(self, course):
        return self.coursesDAO.createOneCourse(course)
