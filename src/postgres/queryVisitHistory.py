import psycopg2 as db

# visit_history table

# 전체 방문 기록 만 불러오기
def getVisitHistoryDict(self, UUID):
    try:
        self.cur.execute("""
        SELECT 
            customer.customer_id,
            customer_data.customer_name,
            customer_data.phone_number, 
            job_list.visit_date
        FROM customer
        INNER JOIN customer_data
        ON ( customer_data.customer_id = customer.customer_id)
        INNER JOIN job_list
        ON ( job_list.customer_id = customer.customer_id )
        WHERE customer.user_id = uuid(%s)""",
        (UUID,))
        return dict(self.cur.fetchall())
    except db.DatabaseError as err:
        print(err)
        return None

# 특정 손님 방문 기록 불러오기
def getVisitHistory(self, customerID):
    try:
        self.cur.execute("""
        SELECT
            customer_id
            customer_name,
            phoneNumber
        FROM customer
        WHERE customerID = %s
        UNION ALL
        SELECT
            customer_id
            visit_date,
            job_id
        FROM when_visited
        WHERE customerID = %s""",
        (customerID, customerID,))
        return dict(self.cur.fetchall())
    except db.DatabaseError as err:
        print(err)
        return None

# 새 방문 기록 추가
def addNewVisited(self, historyData: dict):
    customerID = historyData['customerID']
    visitDate = historyData['visitDate']
    jobID = historyData['jobID']

    try:
        self.cur.execute("""
        INSERT INTO
            when_visited (
                customer_id,
                visit_date,
                job_id
            )
        VALUES
        (
            %s,
            %s,
            %s)""",
        (customerID, visitDate, jobID,))
        return True
    except db.DatabaseError as err:
        print(err)
        return False
