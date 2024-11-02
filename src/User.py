from flask_login import UserMixin

from db import get_user, new_user, is_admin as db_admin

class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic, balance, admin = False):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic
        self.balance = balance
        self.admin = admin
        self.sid = None

    @staticmethod
    def get(user_id):
        try:
            user = User(user_id, *get_user(user_id))
        except TypeError:
            user = None
        return user

    @staticmethod
    def create(id_, name, email, profile_pic):
        new_user(id_, name, email, profile_pic)

    def is_admin(self):
        return db_admin(self.id)
    
    def get_sid(self):
        return self.sid
    
    def set_sid(sid, self):
        self.sid = sid

    def info(self):
        return {"name" : self.name,
                "balance" : self.balance,
                "sid": self.sid}
    
