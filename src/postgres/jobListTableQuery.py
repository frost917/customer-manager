import psycopg2 as db

# job_list table

# 모든 작업 내역 불러오기
def getJobsDict(self, UUID):
    try:
        self.cur.execute("""
    SELECT 
        customer.customer_id,
        customer_data.customer_name,
        customer_data.phone_number,
        job_list.visit_date,
        job_finished.job_type,
        job_type.job_name,
        job_history.job_price,
        job_history.job_description
    FROM customer
    INNER JOIN job_list
    ON ( job_list.customer_id = customer.customer_id )
    INNER JOIN job_history
    ON ( job_history.job_id = job_list.job_id )
    INNER JOIN job_finished
    ON ( job_finished.job_id = job_list.job_id )
    INNER JOIN job_type
    ON ( job_finished.job_type = job_type.job_type )
    WHERE customer.is_deleted = False AND customer.user_id = %s
    """, (UUID,))
        return dict(self.cur.fetchall())
    except:
        return None

# 특정 손님의 작업 내역 불러오기
def getJobsSpecipic(self, customerID):
    try:
        self.cur.execute("""
    SELECT 
        customer.customer_id,
        customer_data.customer_name,
        customer_data.phone_number,
        job_list.visit_date,
        job_finished.job_type,
        job_type.job_name,
        job_history.job_price,
        job_history.job_description
    FROM customer
    INNER JOIN job_list
    ON ( job_list.customer_id = customer.customer_id )
    INNER JOIN job_history
    ON ( job_history.job_id = job_list.job_id )
    INNER JOIN job_finished
    ON ( job_finished.job_id = job_list.job_id )
    INNER JOIN job_type
    ON ( job_finished.job_type = job_type.job_type )
    WHERE customer.is_deleted = False AND customer.customer_id = %s
    """,(customerID,))
        return dict(self.cur.fetchall())
    except db.DatabaseError as err:
        print(err)
        return None

# 작업 기록 불러오기
def getJobHistory(self, jobID):
    try:
        self.cur.execute("""
    SELECT 
        customer.customer_id,
        customer_data.customer_name,
        customer_data.phone_number,
        job_list.visit_date,
        job_finished.job_type,
        job_type.job_name,
        job_history.job_price,
        job_history.job_description
    FROM customer
    INNER JOIN job_list
    ON ( job_list.customer_id = customer.customer_id )
    INNER JOIN job_history
    ON ( job_history.job_id = job_list.job_id )
    INNER JOIN job_finished
    ON ( job_finished.job_id = job_list.job_id )
    INNER JOIN job_type
    ON ( job_finished.job_type = job_type.job_type )
    WHERE customer.is_deleted = False AND customer.customer_id = %s""",
            (jobID, jobID,))
        return dict(self.cur.fetchall())
    except db.DatabaseError as err:
        print(err)
        return None

# 작업 기록 추가
def addNewJob(self, jobData: dict):
    customerID = jobData['customerID']
    jobID = jobData['jobID']
    jobFinished = jobData['jobFinished']
    jobPrice = jobData['jobPrice']
    jobDescription = jobData['jobDescription']

    try:
        # 작업 기록 생성시 한번에 2개의 테이블 참조할 필요 있음
        # 데이터 연결 => job_list.job_id -> job_history.job_id

        self.cur.execute("""
        WITH data (
            user_id, customer_id, customer_name, phone_number
        ) AS ( VALUES ( 
			uuid(%s), 
			uuid(%s), 
			%s, 
			%s) ), 
        step_one AS (
            INSERT INTO customer ( user_id, customer_id )
            SELECT data.user_id, data.customer_id FROM data )
        INSERT INTO customer_data ( customer_id, customer_name, phone_number )
        SELECT data.customer_id, data.customer_name, data.phone_number
        FROM data


        INSERT INTO job_list ( 
            customer_id, job_id, visit_date )
        VALUE (
            %s, %s, CURRENT_DATE 
        )""",
        (customerID, jobID,))

        self.cur.execute("""
            INSERT INTO job_history 
            ( job_id, job_finished, job_price, job_description )
            VALUE (
                %s, %s, %s, %s
            )""",
            (jobID, jobFinished, jobPrice, jobDescription,))
        return True
    except db.DatabaseError as err:
        print(err)
        return False