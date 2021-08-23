import psycopg2 as db

# UUID는 user_id로 대체
# 기존 user_id는 username으로
# login

# 로그인용 쿼리
def getUserPasswd(self, userID):
    try:
        self.cur.execute("""
            SELECT passwd 
            FROM login
            WHERE username = %s""",
            (userID,))
        return dict(self.cur.fetchone())
    except db.DatabaseError as err:
        print(err)
        return None

# UUID 불러오기
def getUUID(self, userData):
    userID = userData.get("userID")
    passwd = userData.get("passwd")
    try:
        self.cur.execute("""
            SELECT user_id 
            FROM login
            WHERE username = %s, passwd = %s""",
            (userID, passwd,))
        return dict(self.cur.fetchone())
    except db.DatabaseError as err:
        print(err)
        return None
