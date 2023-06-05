from actors.User import User


class UserManager:
    def __init__(self, dao):
        self.user = User(dao.db.user)
        self.dao = self.user.dao

    def get_user_list(self):
        user_list = self.dao.list()

        return user_list

    def signin(self, email, password):
        user = self.dao.getByEmail(email)

        if user is None:
            return False

        user_pass = user['password']  # user pass at
        if user_pass != password:
            return False

        return user

    def logout(self):
        self.user.logout()

    def get_user_by_id(self, id):
        user = self.dao.getById(id)

        return user

    def signup(self, username, email, password):
        user = self.dao.getByEmail(email)

        if user is not None:
            return False

        user_info = {"username": username, "email": email, "password": password}

        new_user = self.dao.add(user_info)

        return new_user
