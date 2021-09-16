import psycopg2 as db

# job_list table

# 모든 작업 내역 불러오기
# flaskGetAllJobHistory
def getJobsDict(self, UUID):
    try:
        self.cur.execute("""
    SELECT 
        customer.customer_id,
        customer_data.customer_name,
        customer_data.phone_number,
        job_list.visit_date,
        job_finished.type_id,
        job_type.job_name,
        job_history.job_price,
        job_history.job_description
    FROM customer
    INNER JOIN customer_data
    ON ( customer_data.customer_id = customer.customer_id )
    INNER JOIN job_list
    ON ( job_list.customer_id = customer.customer_id )
    INNER JOIN job_history
    ON ( job_history.job_id = job_list.job_id )
    INNER JOIN job_finished
    ON ( job_finished.job_id = job_list.job_id )
    INNER JOIN job_type
    ON ( job_finished.type_id = job_type.type_id )
    WHERE customer.is_deleted = False AND customer.user_id = uuid(%s)
    """, (UUID,))
        return dict(self.cur.fetchall())
    except:
        return None

# 특정 손님의 작업 내역 불러오기
# flaskGetSpecJobHistory
def getJobsSingleCustomer(self, customerID):
    try:
        self.cur.execute("""
    SELECT 
        customer.customer_id,
        customer_data.customer_name,
        customer_data.phone_number,
        job_list.visit_date,
        job_finished.type_id,
        job_type.job_name,
        job_history.job_price,
        job_history.job_description
    FROM customer
    INNER JOIN customer_data
    ON ( customer_data.customer_id = customer.customer_id )
    INNER JOIN job_list
    ON ( job_list.customer_id = customer.customer_id )
    INNER JOIN job_history
    ON ( job_history.job_id = job_list.job_id )
    INNER JOIN job_finished
    ON ( job_finished.job_id = job_list.job_id )
    INNER JOIN job_type
    ON ( job_finished.type_id = job_type.type_id )
    WHERE customer.is_deleted = False AND customer.customer_id = %s
    """,(customerID,))
        return self.cur.fetchall()
    except db.DatabaseError as err:
        print(err)
        return None

# 작업 기록 불러오기
# flaskGetJobHistory
def getJobHistory(self, jobID):
    try:
        self.cur.execute("""
    SELECT 
        customer_data.customer_id,
        customer_data.customer_name,
        customer_data.phone_number,
        job_list.visit_date,
        job_finished.type_id,
        job_type.job_name,
        job_history.job_price,
        job_history.job_description
    FROM job_history
    INNER JOIN customer_data
    ON ( customer_data.customer_id = job_list.customer_id )
    INNER JOIN job_list
    ON ( job_list.job_id = job_history.job_id )
    INNER JOIN job_finished
    ON ( job_finished.job_id = job_history.job_id )
    INNER JOIN job_type
    ON ( job_finished.type_id = job_type.type_id )
    WHERE customer.is_deleted = False AND job_history.job_id = uuid(%s)""",
            (jobID,))
        return self.cur.fetchone()
    except db.DatabaseError as err:
        print(err)
        return None

# 작업 기록 추가
# flaskAddJobHistory
def addNewJob(self, jobData: dict):
    customerID = jobData['customerID']
    visitDate = jobData['visitDate']
    jobID = jobData['jobID']
    jobFinished = jobData['jobFinished']
    jobPrice = jobData['jobPrice']
    jobDescription = jobData['jobDescription']

    # 작업 기록 생성시 작업 타입이 리스트로 들어오기 때문에
    # 이거 하나하나 분리해서 작업할 필요가 있음
    try:
        self.cur.execute("""
        WITH data (
            customer_id, job_id, visit_date, job_price, job_description
        ) AS ( VALUES ( 
			uuid(%s), uuid(%s), 
            to_timestamp(%s, 'YYYY-MM-DD'), CAST(%s AS INTEGER), %s) 
        ), create_jobid AS (
            INSERT INTO job_list ( customer_id, job_id, visit_date )
            SELECT customer_id, job_id visit_date FROM data 
        )
        INSERT INTO job_history ( job_id, job_price, job_description )
        SELECT job_id, job_price, job_description FROM data""",
        (customerID, jobID, visitDate, jobPrice, jobDescription, ))

        for jobType in jobFinished:
            self.cur.execute("""
            INSERT INTO job_finished
            ( job_id, type_id )
            VALUE (
                uuid(%s), CAST( %s AS INTEGER )
            )""", (jobID, jobType,))
        return True
    except db.DatabaseError as err:
        print(err)
        return False