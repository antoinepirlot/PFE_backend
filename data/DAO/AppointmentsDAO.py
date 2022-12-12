import psycopg2

from data.services.DALService import DALService
from models.Appointment import Appointment


class AppointmentsDAO:
    def __init__(self):
        self.dal = DALService()

    def get_appointments_from_teacher_and_student(self, id_teacher, id_student):
        sql = "SELECT DISTINCT a.id_course, a.id_student, a.appointment_state, a.appointment_date, a.street, a.number_house, a.box_house " \
              "FROM projet.appointments a, projet.courses c " \
              "WHERE a.id_course = c.id_course AND a.id_student = %(id_student)s AND c.id_teacher = %(id_teacher)s"

        try:
            results = self.dal.execute(sql, {"id_teacher": id_teacher, "id_student": id_student}, True)
            if len(results) == 0:
                return None
            all_appointments = []
            for row in results:
                appointment = Appointment(int(row[0]), int(row[1]), str(row[2]), str(row[3]), str(row[4]), int(row[5]),
                                          str(row[7]))
                all_appointments.append(appointment)
            return all_appointments
        except (Exception, psycopg2.DatabaseError) as e:
            try:
                print("SQL Error [%d]: %s" % (e.args[0], e.args[1]))
                raise e
            except IndexError:
                print("SQL Error: %s" % str(e))
                raise e

    def get_appointments_for_user(self, id_student):
        sql = "SELECT DISTINCT id_course, id_student, appointment_state, appointment_date, street, number_house, box_house " \
              "FROM projet.appointments " \
              "WHERE  id_student = %(id_student)s ORDER BY appointment_state DESC, appointment_date"

        try:
            results = self.dal.execute(sql, {"id_student": id_student}, True)
            if len(results) == 0:
                return None
            all_appointments = []
            for row in results:
                appointment = Appointment(int(row[0]), int(row[1]), str(row[2]), str(row[3]), str(row[4]), int(row[5]),
                                          str(row[6]))
                all_appointments.append(appointment)
            return all_appointments
        except (Exception, psycopg2.DatabaseError) as e:
            try:
                print("SQL Error [%d]: %s" % (e.args[0], e.args[1]))
                raise e
            except IndexError:
                print("SQL Error: %s" % str(e))
                raise e

    def get_appointments_for_user_of_course(self, id_course, id_student):
        sql = "SELECT DISTINCT id_course, id_student, appointment_state, appointment_date, street, number_house, box_house " \
              "FROM projet.appointments " \
              "WHERE  id_course = %(id_course)s AND id_student = %(id_student)s"

        try:

            result = self.dal.execute(sql, {"id_course": id_course, "id_student": id_student}, True)
            if len(result) == 0:
                return None
            result = result[0]
            appointment = Appointment(int(result[0]), int(result[1]), str(result[2]), str(result[3]), str(result[4]),
                                      int(result[5]), str(result[6]))
            return appointment
        except (Exception, psycopg2.DatabaseError) as e:
            try:
                print("SQL Error [%d]: %s" % (e.args[0], e.args[1]))
                raise e
            except IndexError:
                print("SQL Error: %s" % str(e))
                raise e
