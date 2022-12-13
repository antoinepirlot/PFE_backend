class User:
    def __init__(self, id_user, lastname, firstname, email, pseudo, sexe, phone, password):
        self.id_user = id_user
        self.lastname = lastname
        self.firstname = firstname
        self.email = email
        self.pseudo = pseudo
        self.sexe = sexe
        self.phone = phone
        self.password = password
        self._skills = None
        self._average_rating = 0

    @property
    def skills(self):
        return self._skills

    @skills.setter
    def skills(self, skills):
        self._skills = skills

    @property
    def average_rating(self):
        return self._average_rating

    @average_rating.setter
    def average_rating(self, average_rating):
        self._average_rating = average_rating

    def convert_to_json(self, with_password=True):
        """
        Convert the current object into json
        :return: a json that represents the current object
        """
        json = {"id_user": self.id_user,
                "lastname": self.lastname,
                "firstname": self.firstname,
                "email": self.email,
                "pseudo": self.pseudo,
                "sexe": self.sexe,
                "phone": self.phone,
                }
        if self.skills is not None:
            table_skills = []
            for skill in self.skills:
                table_skills.append(skill.convert_to_json())
            json['skills'] = table_skills
            json['average_rating'] = self._average_rating
        if with_password:
            json['password'] = self.password
        return json
