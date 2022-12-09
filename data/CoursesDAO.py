import psycopg2
from flask import abort

import data.database as database
from data.services.DALService import DALService
from models.Course import Course


class CoursesDAO:
    def __init__(self):
        self.dal = DALService()
        pass

    def get_one(self, id_course):
        """
        Get one course from the database
        :param id_course: the id of the requested course
        :return: the course matching with id_course
        """
        sql = """
                SELECT id_category, id_teacher, course_description, price_per_hour, city, country, id_level           
                FROM projet.courses
                WHERE id_course = %(id_course)s;
              """
        values = {"id_course": id_course}
        self.dal.start()
        result = self.dal.commit(sql, values)
        if len(result) == 0:
            return None
        result = result[0]
        course = Course(result[0], result[1], result[2], result[3], result[4], result[5], result[6])
        return course

    def createOneCourse(self, course):
        connection = database.initialiseConnection()
        cursor = connection.cursor()
        sql = """
                INSERT INTO projet.courses (id_category, id_teacher, course_description, price_per_hour, city, country,
                id_level) VALUES( %(id_category)s, %(id_teacher)s, %(course_description)s, %(price_per_hour)s, %(city)s,
                %(country)s, %(id_level)s) RETURNING id_course
              """
        try:
            dico_variables = {"id_category": str(course.id_category), "id_teacher": str(course.id_teacher),
                              "course_description": course.course_description,
                              "price_per_hour": str(course.price_per_hour),
                              "city": course.city, "country": course.country, "id_level": str(course.id_level),
                              }
            cursor.execute(sql, dico_variables)
            connection.commit()
            results = cursor.fetchall()
            course.set_id_course(results[0][0])
            return course
        except (Exception, psycopg2.DatabaseError) as e:
            try:
                print("SQL Error [%d]: %s" % (e.args[0], e.args[1]))
                raise Exception from e
            except IndexError:
                print("SQL Error: %s" % str(e))
                raise Exception from e
        finally:
            cursor.close()
            connection.close()
