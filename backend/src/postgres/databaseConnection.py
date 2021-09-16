import psycopg2
import psycopg2.extras


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            cls._instances[cls].__init__(*args, **kwargs)
 
        return cls._instances[cls]

class PostgresControll(metaclass=Singleton):
    def __init__(self):
        import os

        # DB HOST
        host = os.getenv("DB_HOST")
        database = os.getenv("DB_DATABASE")
        # DB_PORT 환경변수가 없는 경우 기본값 5432 부여
        port = 5432 if os.getenv("DB_PORT") is None else os.getenv("DB_PORT")

        # DB USER
        user = os.getenv("DB_USER")
        passwd = os.getenv("DB_PASSWD")

        try:
            self.dbconn = psycopg2.connect(
                database=database, 
                host=host, 
                port=port, 
                user=user, 
                password=passwd)
            self.cur = self.dbconn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        except psycopg2.DatabaseError as err:
            print(err)

    def __del__(self):
        self.dbconn.commit()
        self.dbconn.close()
        self.cur.close()

    # customer table
    # customer info
    from postgres.queryCustomerData import (addNewCustomer, deleteCustomerData,
                                            getCustomerData, getCustomerDict,
                                            updateCustomerData)
    # job_list table
    from postgres.queryJobs import (addNewJob, getAllJobs,getJobHistorySpec, getJobFinishedArray, getCustomerFromJobID)
    # login table
    from postgres.queryLoginData import addNewUser, getUserPasswd, getUUID
    # visit_history table
    from postgres.queryVisitHistory import getVisitHistory, getVisitHistoryDict

    # # 모든 예약 불러오기
    # def getReserveDict(self, UUID):
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
