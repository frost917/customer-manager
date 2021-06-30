import psycopg2 as db
import os

class Database:
    def __init__(self):
        # DB HOST
        host = os.getenv("DB_HOST")
        database = os.getenv("DB_DATABASE")
        # DB_PORT 환경변수가 없는 경우 기본값 5432 부여
        port = os.getenv("DB_PORT") if os.getenv("DB_PORT") is not None else port = 5432

        # DB USER
        user = os.getenv("DB_USER")
        passwd = os.getenv("DB_PASSWD")
        try:
            self.dbconn = db.connect(database=database, host=host, port=port, user=user, passwd=passwd)
            self.dbconn.autocommit = True
            self.cur = self.dbconn.cursor()
        except db.DatabaseError as err:
            print(err)

    def getCustomerTuple(self, uuid):
        try:
            self.cur.execute("""
                SELECT name,phoneNumber 
                FROM customer
                WHERE uuid = %s""",
                (uuid,))
            return self.cur.fetchall()
        except db.DatabaseError as err:
            print(err)

    def getCustomerID(self, uuid, name):
        try:
            self.cur.execute("""
                SELECT customerID 
                FROM customer
                WHERE uuid = %s, name = %s""",
                (uuid, name,))
            return self.cur.fetchone()
        except db.DatabaseError as err:
            print(err)

    def getJobsTuple(self):