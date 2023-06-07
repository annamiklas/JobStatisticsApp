class UserDao:
    def __init__(self, dao):
        self.db = dao
        self.db.table = "users"

    def getByEmail(self, email):
        q = self.db.query("select * from @table where email='{}'".format(email))

        user = q.fetchone()

        return user

    def add(self, user):
        username = user['username']
        email = user['email']
        password = user['password']

        q = self.db.query(
            "INSERT INTO @table (username, email, password) VALUES('{}', '{}', '{}');".format(username, email, password))
        self.db.commit()

        return q
