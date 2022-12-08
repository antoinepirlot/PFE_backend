from data.CoursesDAO import CoursesDAO


class CoursesService:
    coursesDAO = CoursesDAO()

    def __init__(self):
        pass

    def create_one_course(self, course):
        return self.coursesDAO.createOneCourse(course)
