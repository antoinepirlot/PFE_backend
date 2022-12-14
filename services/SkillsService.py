from data.DAO.SkillsDAO import SkillsDAO
from data.services.DALService import DALService


class SkillsService:

    def __init__(self):
        pass

    def __new__(cls):
        if not hasattr(cls, "_instance"):
            # No instance of SkillsService class, a new one is created
            cls._skills_dao = SkillsDAO()
            cls._dal_service = DALService()
            cls._instance = super(SkillsService, cls).__new__(cls)
        # There's already an instance of SkillsService class, so the existing one is returned
        return cls._instance

    def add_notification(self, skill):
        """
        Add a skill for a user
        :param skill: skill to add
        """
        try:
            self._dal_service.start()
            self._skills_dao.add_skill(skill)
            self._dal_service.commit_transaction()
        except Exception as e:
            self._dal_service.rollback_transaction()
            raise e
