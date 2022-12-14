import psycopg2

from data.services.DALService import DALService
from models.Category import Category


class SkillsDAO:
    def __init__(self):
        pass

    def __new__(cls):
        if not hasattr(cls, "_instance"):
            # No instance of SkillsDAO class, a new one is created
            cls._dal = DALService()
            cls._instance = super(SkillsDAO, cls).__new__(cls)
        # There's already an instance of SkillsDAO class, so the existing one is returned
        return cls._instance

    def add_skill(self, skill):
        """
        Add a skill for a user
        :param skill: skill to add
        """
        sql = """
            INSERT INTO projet.teacher_skills VALUES (%(id_category)s,%(id_teacher)s) 
        """
        values = {"id_category": skill.id_category, "id_teacher": skill.id_teacher}
        self._dal.execute(sql, values)

