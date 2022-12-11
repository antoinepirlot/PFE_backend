import psycopg2

from data.services.DALService import DALService
from models.Course import Course


def _create_course_object(list_of_courses, with_teacher=True):
    """
    Creates a new list of Course. It transforms tuples in Course.
    :param: list_of_courses: list of tuples
    :return: a list of Course.
    """
    courses = []
    for course in list_of_courses:
        if with_teacher:
            courses.append(Course(course[0], course[1], course[2], course[3], course[4], course[5], course[6]))
        else:
            courses.append(Course(course[0], None, course[1], course[2], course[3], course[4], course[5]))
    return courses


class CoursesDAO:

    def __init__(self):
        self._dal_service = DALService()

    # __new__ Redefined to use singleton pattern
    def __new__(cls):
        if not hasattr(cls, "instance"):
            # No instance of CoursesDAO class, a new one is created
            cls.instance = super(CoursesDAO, cls).__new__(cls)
        # There's already an instance of CoursesDAO class, so the existing one is returned
        return cls.instance

    def get_one(self, id_course):
        """
        Get one course from the database
        :param id_course: the id of the requested course
        :return: the course matching with id_course. If there's no course, it returns None
        """
        sql = """
                SELECT id_category, id_teacher, course_description, price_per_hour, city, country, level           
                FROM projet.courses
                WHERE id_course = %(id_course)s;
              """
        values = {"id_course": id_course}
        result = self._dal_service.execute(sql, values, True)
        if len(result) == 0:
            return None
        return _create_course_object(result)[0]

    def get_all_courses_from_teacher(self, id_teacher):
        """
        Get all teacher's courses from the database.
        :param id_teacher:  the teacher's id
        :return: the list of teacher's courses. If there's no courses, it returns None
        """
        sql = """
            SELECT DISTINCT id_category, course_description, price_per_hour, city, country, level
            FROM projet.courses
            WHERE id_teacher = %(id_teacher)s;
        """
        values = {"id_teacher": id_teacher}
        try:
            result = self._dal_service.execute(sql, values, True)
            if len(result) == 0:
                return None
            return _create_course_object(result, False)
        except Exception as e:
            raise e

    def get_all_courses(self):
        sql = """SELECT id_category, course_description, price_per_hour, city, country, level
            FROM projet.courses"""
        try:
            result = self._dal_service.execute(sql, None, True)
            if len(result) == 0:
                return None
            return _create_course_object(result, False)
        except Exception as e:
            raise e

    def create_one_course(self, course):
        """
        Create a course in the database
        :param course: the course to add
        :return: the created course
        """
        sql = """
                INSERT INTO projet.courses (id_category, id_teacher, course_description, price_per_hour, city, country,
                level) VALUES( %(id_category)s, %(id_teacher)s, %(course_description)s, %(price_per_hour)s, %(city)s,
                %(country)s, %(level)s) RETURNING id_course
              """
        dico_variables = {
            "id_category": course.id_category,
            "id_teacher": course.id_teacher,
            "course_description": course.course_description,
            "price_per_hour": course.price_per_hour,
            "city": course.city,
            "country": course.country,
            "level": course.level,
        }
        try:
            result = self._dal_service.execute(sql, dico_variables, True)
            course.set_id_course(result[0][0])
            return course
        except (Exception, psycopg2.DatabaseError) as e:
            try:
                print("SQL Error [%d]: %s" % (e.args[0], e.args[1]))
                raise Exception from e
            except IndexError:
                print("SQL Error: %s" % str(e))
                raise Exception from e
