import psycopg2
import psycopg2.extras
from psycopg2 import pool

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
        from config.secret import dbData

        # # DB HOST
        # host = os.getenv("DB_HOST")
        # database = os.getenv("DB_DATABASE")
        # # DB_PORT 환경변수가 없는 경우 기본값 5432 부여
        # port = 5432 if os.getenv("DB_PORT") is None else os.getenv("DB_PORT")

        host = dbData['DB_HOST']
        database = dbData['DB_DATABASE']
        port = dbData['DB_PORT']

        # # DB USER
        # user = os.getenv("DB_USER")
        # passwd = os.getenv("DB_PASSWD")

        user = dbData['DB_USER']
        passwd = dbData['DB_PASSWD']

        # self.dbconn = pool.ThreadedConnectionPool(1, 5, database=database, 
        #     host=host, 
        #     port=port, 
        #     user=user, 
        #     password=passwd,
        #     sslmode='veryfi-ca',
        #     sslrootcert='/certs/ca.crt',
        #     sslcert='/certs/tls.crt',
        #     sslkey='/certs/tls.key')
        self.dbconn = psycopg2.connect(database=database, 
            host=host, 
            port=port, 
            user=user, 
            password=passwd,
            sslmode='required',
            sslrootcert='/certs/ca.crt',
            sslcert='/certs/tls.crt',
            sslkey='/certs/tls.key')

        # self.cur = self.dbconn.getconn().cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        self.cur = self.dbconn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def __del__(self):
        self.dbconn.closeall()
        self.cur.close()

    # customer table
    # customer info
    from postgres.queryCustomerData import (addNewCustomer, 
    deleteCustomerData,
    getCustomerData, 
    getCustomerDict,
    updateCustomerData)

    # job_list table
    from postgres.queryJobs import (addNewJob, getAllJobs,
    getCustomerFromJobID, 
    getJobFinishedArray,
    getJobHistorySpec, 
    getJobListFromJobID,
    getJobsFromCustomerID)
    
    # login table
    from postgres.queryLoginData import addNewUser, getUserPasswd, getUUID

    # visit_history table
    from postgres.queryVisitHistory import getVisitHistory, getVisitHistoryDict

    # 예약 관련 기능 추가
    from postgres.queryReserve import (
        getAllReserve, 
        getReserveData, 
        getReserveType, 
        addNewReserve, 
        setReserveComplete,
        getReserveFromCustomerID,
        deleteReserveData,
        updateReserveData)

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
