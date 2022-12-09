from data.CoursesDAO import CoursesDAO


class CoursesService:
    coursesDAO = CoursesDAO()

    def __init__(self):
        pass

    def get_one(self, id_course):
        return self.coursesDAO.get_one(id_course)

    def create_one_course(self, course):
        return self.coursesDAO.createOneCourse(course)
