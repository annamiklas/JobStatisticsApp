class UserDao:
    def __init__(self, dao):
        self.db = dao
        self.db.table = "users"

    def list(self):
        users = self.db.query(
            "select @table.id,@table.username,@table.email,@table.bio,@table.mob,@table.lock,@table.created_at,"
            "count(reserve.book_id) as books_owned from @table LEFT JOIN reserve ON reserve.user_id=@table.id GROUP BY "
            "reserve.user_id").fetchall()

        return users

    def getById(self, id):
        q = self.db.query("select * from @table where id='{}'".format(id))

        user = q.fetchone()

        return user

    def getUsersByBook(self, book_id):
        q = self.db.query(
            "select * from @table LEFT JOIN reserve ON reserve.user_id = @table.id WHERE reserve.book_id={}".format(
                book_id))

        user = q.fetchall()

        return user

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

    def update(self, user, _id):
        username = user['username']
        email = user['email']
        password = user['password']
        bio = user['bio']

        q = self.db.query(
            "UPDATE @table SET username = '{}', email='{}', password='{}', bio='{}' WHERE id={}".format(username, email,
                                                                                                    password, bio, _id))
        self.db.commit()

        return q
