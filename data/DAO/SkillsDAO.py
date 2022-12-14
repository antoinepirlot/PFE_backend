import psycopg2

from data.services.DALService import DALService
from models.Category import Category


class SkillsDAO:
    def __init__(self):
        self._dal_service = DALService()

    def add_skill(self, skill):
        """
        Add a skill for a user
        :param skill: skill to add
        """
        sql = """
            INSERT INTO projet.teacher_skills VALUES (%(id_category)s,%(id_teacher)s) 
        """
        values = {"id_category": skill.id_category, "id_teacher": skill.id_teacher}
        self._dal_service.execute(sql, values)

