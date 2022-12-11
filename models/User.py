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

    def convert_to_json(self, with_password=True):
        json = {"id_user": self.id_user,
                "lastname": self.lastname,
                "firstname": self.firstname,
                "email": self.email,
                "pseudo": self.pseudo,
                "sexe": self.sexe,
                "phone": self.phone,
                }
        if with_password:
            json['password'] = self.password
        return json
