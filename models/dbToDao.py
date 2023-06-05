from copy import copy

from models.UserDao import UserDao
from models.dbConnection import DbConnection


class DbToDao(DbConnection):

    def __init__(self, app):
        super(DbToDao, self).__init__(app)
        self.user = UserDao(copy(self))
