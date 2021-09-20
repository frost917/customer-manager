import psycopg2 as db

# UUID는 user_id로 대체
# 기존 user_id는 username으로
# login

# 유저 데이터 생성하는 함수
def addNewUser(self, userData):
    userID = userData.get("UUID")
    username = userData.get("userID")
    passwd = userData.get("passwd")

    self.cur.execute("""
        INSERT INTO
            login
        (
            user_id,
            username,
            passwd
        )
        VALUES
        (
            uuid(%s),
            %s,
            %s
        )""",
        (userID, username, passwd,))

# 로그인용 쿼리
def getUserPasswd(self, userID):
    try:
        self.cur.execute("""
            SELECT passwd 
            FROM login
            WHERE username = %s""",
            (userID,))
        return self.cur.fetchone()
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
            WHERE username = %s AND passwd = %s""",
            (userID, passwd,))
        result = self.cur.fetchone()
        if result is None:
            result = dict()
        return result
    except db.DatabaseError as err:
        print(err)
        return None
