import psycopg2 as db
import os

class PostgresControll:
    def __init__(self):
        # DB HOST
        host = os.getenv("DB_HOST")
        database = os.getenv("DB_DATABASE")
        # DB_PORT 환경변수가 없는 경우 기본값 5432 부여
        port = 5432 if os.getenv("DB_PORT") is None else os.getenv("DB_PORT")

        # DB USER
        user = os.getenv("DB_USER")
        passwd = os.getenv("DB_PASSWD")
        try:
            self.dbconn = db.connect(
                database=database, 
                host=host, 
                port=port, 
                user=user, 
                passwd=passwd)
            self.dbconn.autocommit = True
            self.cur = self.dbconn.cursor()
        except db.DatabaseError as err:
            print(err)

    # login

    # 로그인용 쿼리
    def getUserPasswd(self, userID):
        try:
            self.cur.execute("""
                SELECT passwd 
                FROM login
                WHERE userID = %s""",
                (userID,))
            return self.cur.fetchone()
        except db.DatabaseError as err:
            print(err)

    # UUID 불러오기
    def getUUID(self, userID, passwd):
        try:
            self.cur.execute("""
                SELECT UUID 
                FROM login
                WHERE userID = %s, passwd = %s""",
                (userID, passwd,))
            return self.cur.fetchone()
        except db.DatabaseError as err:
            print(err)

    # customer table

    # 고객 명단 불러오기
    def getCustomerTuple(self, UUID):
        try:
            self.cur.execute("""
                SELECT customerID,name,phoneNumber 
                FROM customer
                WHERE UUID = %s""",
                (UUID,))
            return self.cur.fetchall()
        except db.DatabaseError as err:
            print(err)

    # 새 고객 추가
    def addNewCustomer(self, UUID, customerID, name, phoneNumber):
        try:
            self.cur.execute("""
            INSERT INTO
                customer (
                    UUID,
                    customerID,
                    name,
                    phoneNumber
                )
            VALUES (
                %s,
                %s,
                %s,
                %s
                )""",
            (UUID, customerID, name, phoneNumber,)
            )
        except db.DatabaseError as err:
            print(err)

    # 고객 ID 불러오기
    def getCustomerID(self, UUID, name):
        try:
            self.cur.execute("""
                SELECT customerID 
                FROM customer
                WHERE UUID = %s AND name = %s""",
                (UUID, name,))
            return self.cur.fetchone()
        except db.DatabaseError as err:
            print(err)

    # when_visited table

    # 전체 방문 기록 만 불러오기
    def getVisitedTuple(self, UUID):
        try:
            self.cur.execute("""
            SELECT
                customerID,
                name,
                phoneNumber
            FROM customer
            WHERE UUID = %s
            UNION ALL
            SELECT
                customerID,
                visitDate,
                jobID
            FROM when_visited""",
            (UUID,))
        except db.DatabaseError as err:
            print(err)

    # 특정 손님 방문 기록 불러오기
    def getVisitedTuple(self, customerID):
        try:
            self.cur.execute(
            # SELECT
            #     name,
            #     phoneNumber
            # FROM customer
            # WHERE customerID = %s
            # UNION
            """
            SELECT
                visitDate,
                jobID
            FROM when_visited
            WHERE customerID = %s""",
            (customerID, customerID,))
        except db.DatabaseError as err:
            print(err)

    # 새 방문 기록 추가
    def addNewVisited(self, customerID, jobID):
        try:
            self.cur.execute("""
            INSERT INTO
                when_visited (
                    customerID,
                    visitDate,
                    jobID
                )
            VALUES
            (
                %s,
                CURRENT_DATE,
                %s)""",
            (customerID, jobID,))
        except db.DatabaseError as err:
            print(err)

    # job_list table

    # 모든 작업 내역 불러오기
    def getJobsTuple(self, UUID):
        try:
            self.cur.execute("""
                SELECT
                    name,
                    phoneNumber
                FROM customer
                WHERE UUID = %s
                SELECT 
                    jobID,
                    jobs
                FROM jobs_list
                where UUID = %s""",
                (UUID, UUID,))
        except db.DatabaseError as err:
            print(err)

    # 특정 손님의 작업 내역 불러오기
    def getJobsSpecipic(self, UUID, customerID):
        try:
            self.cur.execute("""
                SELECT jobID, jobs
                FROM jobs_list
                WHERE UUID = %s AND customerID = %s""",
                (UUID, customerID,))
        except db.DatabaseError as err:
            print(err)
    
    # 작업 기록 불러오기
    def getJobHistory(self, jobID):
        try:
            self.cur.execute("""
                SELECT
                    name,
                    phoneNumber
                FROM customer
                WHERE customerID IN (
                    SELECT customerID
                    FROM when_visited
                    WHERE jobID = %s
                )
                UNION ALL
                SELECT 
                    jobPrice,
                    jobHistory
                FROM job_history
                where jobID = %s""",
                (jobID, jobID,))
        except db.DatabaseError as err:
            print(err)

    # # 모든 예약 불러오기
    # def getReserveTuple(self, UUID):
    #     try:
    #         self.cur.execute("""
    #             SELECT 
    #             SELECT customerID, reservedTime
    #             FROM reserve
    #             where UUID = %s""",
    #             (UUID,))
    #     except db.DatabaseError as err:
    #         print(err)

    # # 특정 손님의 예약 불러오기
    # def getReserveSpecipic(self, UUID):
    #     try:
    #         self.cur.execute("""
    #             SELECT customerID, reservedTime
    #             FROM reserve
    #             where UUID = %s""",
    #             (UUID,))
    #     except db.DatabaseError as err:
    #         print(err)