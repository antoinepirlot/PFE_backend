from data.services.DALService import DALService
from models.Favorite import Favorite


class FavoritesDAO:
    def __init__(self):
        pass

    def __new__(cls):
        if not hasattr(cls, "_instance"):
            # No instance of FavoritesDAO class, a new one is created
            cls._dal = DALService()
            cls._instance = super(FavoritesDAO, cls).__new__(cls)
        # There's already an instance of FavoritesDAO class, so the existing one is returned
        return cls._instance

    def get_favorite(self, id_teacher, id_student):
        """
        Get the favorite retrieved by its id_teacher and id_student
        :param id_teacher: the id of the teacher
        :param id_student: the id of the student
        :return: the favorite
        """
        sql = """
            SELECT id_student, id_teacher FROM projet.favorites 
            WHERE id_student = %(id_student)s AND id_teacher = %(id_teacher)s
        """
        values = {"id_student": id_student, "id_teacher": id_teacher}
        result = self._dal.execute(sql, values, True)
        if len(result) == 0:
            return None
        result = result[0]
        favorite = Favorite(int(result[0]), int(result[1]))
        return favorite

    def get_favorite_teachers_from_user(self, id_student):
        """
        Get all favorites from a specific user
        :param id: the id of the user
        :return: list of all his favorite or None
        """
        sql = """
            SELECT id_teacher, id_student 
            FROM projet.favorites 
            WHERE id_student = %(id_student)s
        """
        values = {"id_student": id_student}
        results_export_fav_teachers = []
        results = self._dal.execute(sql, values, True)
        for row in results:
            favorite = Favorite(int(row[0]), int(row[1]))
            results_export_fav_teachers.append(favorite)
        return results_export_fav_teachers

    def get_most_favorites_teachers(self):
        """
        Get a list with the id teacher and its number of favorites student gives to him foreach teacher
        :return: list with the id teacher and its number of favorites student gives to him foreach teacher
        """
        sql = """
            SELECT id_teacher, count(id_student) as total FROM projet.favorites 
            GROUP BY id_teacher ORDER BY total DESC
        """
        results_export_fav_teachers = []
        results = self._dal.execute(sql, [], True)
        if len(results) == 0:
            return None
        for row in results:
            res = {
                "id_teacher": row[0],
                "total_like": row[1]
            }
            results_export_fav_teachers.append(res)
        return results_export_fav_teachers

    def add_favorite(self, favorite):
        """
        Create a favorite
        :param favorite: the favorite we want to add
        :return: the created favorite
        """
        sql = """
            INSERT INTO projet.favorites(id_teacher, id_student)
            VALUES( %(id_teacher)s, %(id_student)s)
            RETURNING id_teacher, id_student
        """

        values = {"id_teacher": int(favorite.id_teacher), "id_student": int(favorite.id_student)}
        results = self._dal.execute(sql, values, True)
        if len(results) == 0:
            return None
        return Favorite(results[0][0], results[0][1])

    def remove_favorite(self, id_teacher, id_student):
        """
        Remove a favorite
        :param id_teacher: the id of the teacher
        :param id_student: the id of the student
        """
        sql = """
            DELETE FROM projet.favorites 
            WHERE id_student = %(id_student)s AND id_teacher = %(id_teacher)s
        """
        values = {"id_student": id_student, "id_teacher": id_teacher}
        self._dal.execute(sql, values)
