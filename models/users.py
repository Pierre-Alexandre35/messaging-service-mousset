import uuid

class User():
    def __init__(self, title, first_name, last_name, email, password, id=""):
        self.title = title
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.id = uuid.uuid4().hex if not id else id

    def dict(self):
        return {
        "id" : self.id,
        "title" : self.title,
        "first_name" : self.first_name,
        "last_name" : self.last_name,
        "email" : self.email,
        "password" : self.password
        }

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


class Anonymous():

    @property
    def is_authenticated(self):
        return False

    @property
    def is_active(self):
        return False

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return None
