from data.DAO.SkillsDAO import SkillsDAO
from data.services.DALService import DALService


class SkillsService:
    _skills_dao = SkillsDAO()
    _dal_service = DALService()

    def __init__(self):
        pass

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
