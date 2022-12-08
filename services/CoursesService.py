from data.CoursesDAO import CoursesDAO


class CoursesService:
    coursesDAO = CoursesDAO()

    def __init__(self):
        pass

    def get_one(self, id_course):
        result = self.coursesDAO.get_one(id_course)
        return result


    def create_one_course(self, course):
        return self.coursesDAO.createOneCourse(course)
