import psycopg2 as db

# job_list table

# 모든 작업 내역 불러오기
def getJobsDict(self, UUID):
    try:
        self.cur.execute("""
            SELECT
                customer_name,
                phone_number
            FROM customer
            WHERE user_id = %s
            SELECT 
                job_id,
                jobs_finish
            FROM job_list
            where user_id = %s""",
            (UUID, UUID,))
        return dict(self.cur.fetchall())
    except db.DatabaseError as err:
        print(err)
        return None

# 특정 손님의 작업 내역 불러오기
def getJobsSpecipic(self, UUID, customerID):
    try:
        self.cur.execute("""
            SELECT job_id, jobs
            FROM job_list
            WHERE user_id = %s AND customer_id = %s""",
            (UUID, customerID,))
        return dict(self.cur.fetchall())
    except db.DatabaseError as err:
        print(err)
        return None

# 작업 기록 불러오기
def getJobHistory(self, jobID):
    try:
        self.cur.execute("""
            SELECT
                customer_name,
                phone_number
            FROM customer
            WHERE customer_id IN (
                SELECT customer_id
                FROM when_visited
                WHERE job_id = %s
            )
            UNION ALL
            SELECT 
                job_price,
                job_history
            FROM job_history
            where job_id = %s""",
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