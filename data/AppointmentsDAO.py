from flask import abort

import data.database as database
from models.Appointment import Appointment
import psycopg2


class AppointmentsDAO:
    def __init__(self):
        pass

    def get_appointments_from_teacher_and_student(self, id_teacher, id_student):
        connection = database.initialiseConnection()
        cursor = connection.cursor()
        sql = "SELECT DISTINCT a.id_course, a.id_student, a.appointment_state, a.appointment_date, a.street, a.number_house, a.box_house " \
              "FROM projet.appointments a, projet.courses c " \
              "WHERE a.id_course = c.id_course AND a.id_student = %(id_student)s AND c.id_teacher = %(id_teacher)s"

        try:
            cursor.execute(sql, {"id_teacher": id_teacher, "id_student": id_student})
            connection.commit()
            results = cursor.fetchall()
            if len(results) == 0:
                abort(404, "Appointment not found")
            all_appointments = []
            for row in results:
                appointment = Appointment(int(row[0]), int(row[1]), str(row[2]), str(row[3]), str(row[4]), int(row[5]), str(row[1]))
                all_appointments.append(appointment)
            return all_appointments
        except (Exception, psycopg2.DatabaseError) as e:
            try:
                print("SQL Error [%d]: %s" % (e.args[0], e.args[1]))
                raise e
            except IndexError:
                print("SQL Error: %s" % str(e))
                raise e
        finally:
            cursor.close()
            connection.close()