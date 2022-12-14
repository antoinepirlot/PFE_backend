class User:
    def __init__(self, id_user, lastname, firstname, email, pseudo, sexe, phone, password):
        self._id_user = id_user
        self._lastname = lastname
        self._firstname = firstname
        self._email = email
        self._pseudo = pseudo
        self._sexe = sexe
        self._phone = phone
        self._password = password
        self._skills = None
        self._average_rating = 0

    @property
    def id_user(self):
        return self._id_user

    @property
    def lastname(self):
        return self._lastname

    @property
    def firstname(self):
        return self._firstname

    @property
    def email(self):
        return self._email

    @property
    def pseudo(self):
        return self._pseudo

    @property
    def sexe(self):
        return self._sexe

    @property
    def phone(self):
        return self._phone

    @property
    def password(self):
        return self._password

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
