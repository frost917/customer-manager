import psycopg2 as db
# visit_history table

# 전체 방문 기록 만 불러오기
def getVisitHistoryDict(self, UUID):
    try:
        self.cur.execute("""
        SELECT
            customer_id,
            name,
            phone_number
        FROM customer
        WHERE UUID = %s
        UNION ALL
        SELECT
            customer_id,
            visit_date,
            job_id
        FROM when_visited""",
        (UUID,))
        return self.cur.fetchall()
    except db.DatabaseError as err:
        print(err)
        return None

# 특정 손님 방문 기록 불러오기
def getVisitHistory(self, customerID):
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
            visit_date,
            job_id
        FROM when_visited
        WHERE customerID = %s""",
        (customerID, customerID,))
        return self.cur.fetchall()
    except db.DatabaseError as err:
        print(err)
        return None

# 새 방문 기록 추가
def addNewVisited(self, customerID, jobID):
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
            CURRENT_DATE,
            %s)""",
        (customerID, jobID,))
        return True
    except db.DatabaseError as err:
        print(err)
        return False
