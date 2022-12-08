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

    @classmethod
    def init_user_with_json(cls, json):
        return cls(json["id_user"], json["lastname"], json["firstname"], json["email"], json["pseudo"], json["sexe"],
                   json["phone"], json["password"])

    def convert_to_json(self):
        return {"id_user": self.id_user,
                "lastname": self.lastname,
                "firstname": self.firstname,
                "email": self.email,
                "pseudo": self.pseudo,
                "sexe": self.sexe,
                "phone": self.phone,
                "password": self.password
                }
