from Exceptions.WebExceptions.NotFoundException import NotFoundException
from data.services.DALService import DALService
from models.Category import Category
from models.Course import Course
from models.User import User


def _create_course_object(list_of_courses):
    """
    Creates a new list of Course. It transforms tuples in Course. //!\\ Be careful with order in sql query
    :param: list_of_courses: list of tuples
    :return: a list of Course.
    """
    courses = []
    for course in list_of_courses:
        teacher = User(course[9], course[10], course[11], course[12], course[13], course[14], course[15], None)
        category = Category(course[6], course[7], course[8])
        c = Course(category, teacher, course[1], course[2], course[3], course[4], course[5])
        c.id_course = course[0]
        courses.append(c)
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
                SELECT cou.id_course, cou.course_description, cou.price_per_hour, cou.city, cou.country, cou.level,
                   cat.id_category, cat.name, cat.color,
                   u.id_user, u.lastname, u.firstname, u.email, u.pseudo, u.sexe, u.phone          
                FROM projet.courses cou, projet.users u, projet.categories cat
                WHERE cou.id_teacher = u.id_user
                  AND cou.id_category = cat.id_category
                  AND id_course = %(id_course)s;
              """
        values = {"id_course": id_course}
        result = self._dal_service.execute(sql, values, True)
        if len(result) == 0:
            return None
        return _create_course_object(result)[0]

    def get_all_courses_from_teacher(self, id_teacher):
        """
        Get all teacher's courses from the database.
        :param: id_teacher:  the teacher's id
        :return: the list of teacher's courses. If there's no courses, it returns None
        """
        sql = """
            SELECT cou.id_course, cou.course_description, cou.price_per_hour, cou.city, cou.country, cou.level,
                   cat.id_category, cat.name, cat.color,
                   u.id_user, u.lastname, u.firstname, u.email, u.pseudo, u.sexe, u.phone
            FROM projet.courses cou, projet.users u, projet.categories cat
            WHERE cou.id_teacher = u.id_user
              AND cou.id_category = cat.id_category
              AND id_teacher = %(id_teacher)s;
        """
        values = {"id_teacher": id_teacher}
        result = self._dal_service.execute(sql, values, True)
        if len(result) == 0:
            raise NotFoundException
        return _create_course_object(result)

    def get_all_courses(self):
        sql = """
                SELECT cou.id_course, cou.course_description, cou.price_per_hour, cou.city, cou.country, cou.level,
                       cat.id_category, cat.name, cat.color,
                       u.id_user, u.lastname, u.firstname, u.email, u.pseudo, u.sexe, u.phone
                FROM projet.courses cou, projet.users u, projet.categories cat
                WHERE cou.id_teacher = u.id_user
                  AND cou.id_category = cat.id_category
            """

        result = self._dal_service.execute(sql, None, True)
        if len(result) == 0:
            raise NotFoundException
        return _create_course_object(result)

    # def get_all_courses(self):
    #     """
    #     Get courses from DAO and convert them to json
    #     :return: the list of converted courses in json
    #     """
    #     courses = None
    #     try:
    #         self._dal_service.start()
    #         courses = self._courses_dao.get_all_courses()
    #         self._dal_service.commit_transaction()
    #     except Exception as sql_error:  # TODO maybe psycopg2.Error
    #         self._dal_service.rollback_transaction()
    #     if courses is not None:
    #         return convert_models_objects_to_json(courses)
    #     return None

    def create_one_course(self, course):
        """
        Create a course in the database
        :param course: the course to add
        :return: the created course
        """
        sql = """
                    INSERT INTO projet.courses (id_category, id_teacher, course_description, price_per_hour, city, country,
                    level) VALUES( %(id_category)s, %(id_teacher)s, %(course_description)s, %(price_per_hour)s, %(city)s,
                    %(country)s, %(level)s) RETURNING id_course;
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
        result = self._dal_service.execute(sql, dico_variables, True)
        course.id_course = result[0][0]
        return course
