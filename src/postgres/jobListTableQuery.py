import psycopg2 as db

# job_list table

# 모든 작업 내역 불러오기
def getJobsDict(self, UUID):
    try:
        self.cur.execute("""
            SELECT
                name,
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
                name,
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
