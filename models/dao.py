from models.dbToDao import DbToDao


class Dao:

    def __init__(self, app):
        self.db = DbToDao(app)
