import psycopg2

import data.database as database
from models.Category import Category


class CategoriesDAO:
    def __init__(self):
        pass

    def get_all_categories(self):
        connection = database.initialiseConnection()
        cursor = connection.cursor()
        sql = "SELECT id_category, name FROM projet.categories "
        try:
            cursor.execute(sql, None)
            connection.commit()
            results = cursor.fetchall()
            all_categories = []
            for row in results:
                rating = Category(int(row[0]), str(row[1]))
                all_categories.append(rating)
            return all_categories
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
