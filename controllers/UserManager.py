from passlib.handlers.pbkdf2 import pbkdf2_sha256

from actors.User import User


class UserManager:
    def __init__(self, dao):
        self.user = User(dao.db.user)
        self.dao = self.user.dao

    def signin(self, email, password):
        user = self.dao.getByEmail(email)

        if user is None:
            return False

        user_pass = user['password']
        if not pbkdf2_sha256.verify(password, user_pass):
            return False

        return user

    def logout(self):
        self.user.logout()

    def signup(self, username, email, password):
        user = self.dao.getByEmail(email)

        if user is not None:
            return False

        user_info = {"username": username, "email": email, "password": password}

        new_user = self.dao.add(user_info)

        return new_user
