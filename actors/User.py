from actors.Actor import Actor


class User(Actor):
    id = 0
    name = ""
    lock = False

    user = {}

    def __init__(self, user_dao):
        self.dao = user_dao
        self.sess_key = "user"
