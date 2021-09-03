import psycopg2 as db

# customer table

# 고객 명단 불러오기
def getCustomerDict(self, UUID):
    try:
        self.cur.execute("""
            SELECT customer_id,customer_name,phone_number 
            FROM customer
            WHERE user_id = %s""",
            (UUID,))
        return dict(self.cur.fetchall())
    except db.DatabaseError as err:
        print(err)
        return None

def getCustomerData(self, userData):
    UUID = userData["UUID"]
    customerID = userData["customerID"]

    try:
        self.cur.execute("""
            SELECT 
                customer_name,
                phone_number 
            FROM customer_data
            WHERE customer_id = %s""",
            (UUID, customerID,))
        return dict(self.cur.fetchone())
    except db.DatabaseError as err:
        print(err)
        return None

# 새 고객 추가
def addNewCustomer(self, userData):
    UUID = userData["UUID"]
    customerID = userData["customerID"]
    customerName = userData["customerName"]
    phoneNumber = userData["phoneNumber"]

    try:
        self.cur.execute("""
        WITH data (
            user_id, customer_id, customer_name, phone_number
        ) AS ( VALUES ( uuid(%s), uuid(%s), %s, %s) ), 
        step_one AS (
            INSERT INTO customer ( user_id, customer_id )
            SELECT data.user_id, data.customer_id FROM data )
        INSERT INTO customer_data ( customer_id, customer_name, phone_number )
        SELECT data.customer_id, data.customer_name, data.phone_number
        FROM data
        """,
        (UUID, customerID, customerName, phoneNumber,))
        return True
    except db.DatabaseError as err:
        print(err)
        return False

# 고객 ID 불러오기
def getCustomerID(self, userData):
    UUID = userData["UUID"]
    customerName = userData["customerName"]
    phoneNumber = userData["phoneNumber"]

    try:
        self.cur.execute("""
            SELECT customer_id 
            FROM customer
            WHERE user_id = %s AND customer_name = %s AND phone_number = %s""",
            (UUID, customerName, phoneNumber,))
        return dict(self.cur.fetchone())
    except db.DatabaseError as err:
        print(err)
        return None

def updateCustomerData(self, customerData):
    customerID = customerData["customerID"]
    customerName = customerData["customerName"]
    phoneNumber = customerData["phoneNumber"]

    try:
        self.cur.execute("""
            UPDATE 
                customer 
            SET
                customer_name = %s,
                phone_number = %s
            WHERE customer_id = %s""",
            (customerName, phoneNumber, customerID,))
        return True
    except db.DatabaseError as err:
        print(err)
        return False

# customer table의 is_deleted 항목을 True로 변경
def deleteCustomerData(self, customerData):
    customerID = customerData["customerID"]
    try:
        self.cur.execute("""
        UPDATE
            customer
        SET
            is_deleted = True
        WHERE customer_id = %s""",
        (customerID,))
        return True
    except db.DatabaseError as err:
        print(err)
        return False

# 손님 데이터를 진짜로 삭제함
def removeCustomerData(self, customerData):
    customerID = customerData["customerID"]
    try:
        self.cur.execute("""
        WITH data (
            customer_id
        ) AS ( VALUES ( uuid(%s) ) ), 
        step_one AS (
            DELETE FROM customer_data
            WHERE customer_id IN (SELECT data.customer_id FROM data)
        )
        DELETE FROM customer
        WHERE customer_id IN (SELECT data.customer_id FROM data)""",
        (customerID,))
        return True
    except db.DatabaseError as err:
        print(err)
        return False
