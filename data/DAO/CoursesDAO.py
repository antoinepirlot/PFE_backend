from Exceptions.WebExceptions.NotFoundException import NotFoundException
from data.services.DALService import DALService
from models.Category import Category
from models.Course import Course
from models.User import User


def _create_course_object(list_of_courses, handle_stars=False):
    """
    Creates a new list of Course. It transforms tuples in Course. //!\\ Be careful with order in sql query
    :param: list_of_courses: list of tuples
    :return: a list of Course.
    """
    courses = []
    for course in list_of_courses:
        teacher = User(course[8], course[9], course[10], course[11], course[12], course[13], course[14], None)
        category = Category(course[6], course[7])
        if handle_stars:
            c = Course(category, teacher, course[1], course[2], course[3], course[4], course[5], course[15], course[16])
        else:
            c = Course(category, teacher, course[1], course[2], course[3], course[4], course[5])
        c.id_course = course[0]
        courses.append(c)
    return courses


class CoursesDAO:

    def __init__(self):
        pass

    # __new__ Redefined to use singleton pattern
    def __new__(cls):
        if not hasattr(cls, "_instance"):
            # No instance of CoursesDAO class, a new one is created
            cls._dal = DALService()
            cls._instance = super(CoursesDAO, cls).__new__(cls)
        # There's already an instance of CoursesDAO class, so the existing one is returned
        return cls._instance

    def get_one(self, id_course):
        """
        Get one course from the database
        :param id_course: the id of the requested course
        :return: the course matching with id_course. If there's no course, it returns None
        """
        sql = """
                SELECT
                   cou.id_course, cou.course_description, cou.price_per_hour, cou.city, cou.country, cou.level,
                   cat.id_category, cat.name,u.id_user, u.lastname, u.firstname, u.email, u.pseudo, u.sexe, u.phone,
                   COALESCE(SUM(ra.rating_number),0) AS "sum_stars", COUNT(ra.id_rated) AS "total_tuples_stars"
                FROM 
                   projet.categories cat LEFT OUTER JOIN projet.courses cou ON cou.id_category = cat.id_category
                   LEFT OUTER JOIN projet.users u ON cou.id_teacher = u.id_user
                   LEFT OUTER JOIN projet.ratings ra ON u.id_user = ra.id_rated 
                WHERE id_course = %(id_course)s
                GROUP BY cou.id_course, cat.id_category, u.id_user;
              """
        values = {"id_course": id_course}
        result = self._dal.execute(sql, values, True)
        if len(result) == 0:
            return None
        return _create_course_object(result, True)[0]

    def get_all_courses_from_teacher(self, id_teacher):
        """
        Get all teacher's courses from the database.
        :param: id_teacher:  the teacher's id
        :return: the list of teacher's courses. If there's no courses, it returns None
        """
        sql = """
            SELECT
                   cou.id_course, cou.course_description, cou.price_per_hour, cou.city, cou.country, cou.level,
                   cat.id_category, cat.name,u.id_user, u.lastname, u.firstname, u.email, u.pseudo, u.sexe, u.phone,
                   COALESCE(SUM(ra.rating_number),0) AS "sum_stars", COUNT(ra.id_rated) AS "total_tuples_stars"
                FROM 
                   projet.categories cat LEFT OUTER JOIN projet.courses cou ON cou.id_category = cat.id_category
                   LEFT OUTER JOIN projet.users u ON cou.id_teacher = u.id_user
                   LEFT OUTER JOIN projet.ratings ra ON u.id_user = ra.id_rated 
                WHERE id_teacher = %(id_teacher)s
                GROUP BY cou.id_course, cat.id_category, u.id_user;
        """
        values = {"id_teacher": id_teacher}
        result = self._dal.execute(sql, values, True)
        if len(result) == 0:
            raise NotFoundException
        return _create_course_object(result, True)

    def get_all_courses(self, filter=None):
        """
        Get all courses with a filter or not
        :param filter: by what you want to filter all courses (here for course category, course description, city)
        :return: all courses with the potential filter applied
        """
        filter_match_table_db = {
            "course": "cat.name",
            "description": "cou.course_description",
            "city": "cou.city"
        }

        sql = """
                SELECT
                   cou.id_course, cou.course_description, cou.price_per_hour, cou.city, cou.country, cou.level,
                   cat.id_category, cat.name,u.id_user, u.lastname, u.firstname, u.email, u.pseudo, u.sexe, u.phone,
                   COALESCE(SUM(ra.rating_number),0) AS "sum_stars", COUNT(ra.id_rated) AS "total_tuples_stars"
                FROM 
                   projet.categories cat LEFT OUTER JOIN projet.courses cou ON cou.id_category = cat.id_category
                   LEFT OUTER JOIN projet.users u ON cou.id_teacher = u.id_user
                   LEFT OUTER JOIN projet.ratings ra ON u.id_user = ra.id_rated 
                
            """

        values = {}

        number_of_filter = 0
        if filter is not None:
            for filter_objet in filter:
                key_filter = list(filter_objet.keys())[0]
                name_field = filter_match_table_db[key_filter]
                value_filter = list(filter_objet.values())[0]
                if number_of_filter == 0:
                    sql += f"""WHERE LOWER({name_field}) LIKE LOWER(%({number_of_filter})s) """
                else:
                    sql += f"""AND LOWER({name_field}) LIKE LOWER(%({number_of_filter})s) """
                values.update({f'{number_of_filter}': '%'+value_filter+'%'})
                number_of_filter += 1

        sql += "GROUP BY cou.id_course, cat.id_category, u.id_user;"


        result = self._dal.execute(sql, values, True)
        if len(result) == 0:
            raise NotFoundException
        return _create_course_object(result, True)

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
        result = self._dal.execute(sql, dico_variables, True)
        course.id_course = result[0][0]
        return course
