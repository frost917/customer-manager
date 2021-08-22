import psycopg2 as db
# login

# 로그인용 쿼리
def getUserPasswd(self, userID):
    try:
        self.cur.execute("""
            SELECT passwd 
            FROM login
            WHERE userID = %s""",
            (userID,))
        return tuple(self.cur.fetchone())
    except db.DatabaseError as err:
        print(err)
        return None

# UUID 불러오기
def getUUID(self, userID, passwd):
    try:
        self.cur.execute("""
            SELECT UUID 
            FROM login
            WHERE user_id = %s, passwd = %s""",
            (userID, passwd,))
        return self.cur.fetchone()
    except db.DatabaseError as err:
        print(err)
        return None
