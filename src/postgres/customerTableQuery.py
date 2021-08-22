import psycopg2 as db
# customer table

# 고객 명단 불러오기
def getCustomerTuple(self, UUID):
    try:
        self.cur.execute("""
            SELECT customer_id,name,phone_number 
            FROM customer
            WHERE UUID = %s""",
            (UUID,))
        return self.cur.fetchall()
    except db.DatabaseError as err:
        print(err)
        return None

def getCustomerInfo(self, UUID, customerID):
    try:
        self.cur.execute("""
            SELECT name,phone_number 
            FROM customer
            WHERE UUID = %s AND customer_id = %s""",
            (UUID, customerID,))
        return tuple(self.cur.fetchone())
    except db.DatabaseError as err:
        print(err)
        return None

# 새 고객 추가
def addNewCustomer(self, UUID, customerID, name, phoneNumber):
    try:
        self.cur.execute("""
        INSERT INTO
            customer (
                UUID,
                customer_id,
                name,
                phone_number
            )
        VALUES (
            %s,
            %s,
            %s,
            %s
            )""",
        (UUID, customerID, name, phoneNumber,))
        return True
    except db.DatabaseError as err:
        print(err)
        return False

# 고객 ID 불러오기
def getCustomerID(self, UUID, name):
    try:
        self.cur.execute("""
            SELECT customer_id 
            FROM customer
            WHERE UUID = %s AND name = %s""",
            (UUID, name,))
        return self.cur.fetchone()
    except db.DatabaseError as err:
        print(err)
        return None

def updateCustomerInfo(self, UUID, customerData):
    customerID = customerData["customerID"]
    name = customerData["name"]
    phoneNumber = customerData["phoneNumber"]

    try:
        self.cur.execute("""
            SELECT customer_id 
            FROM customer
            WHERE UUID = %s AND name = %s""",
            (name, phoneNumber, UUID,))
        return self.cur.fetchone()
    except db.DatabaseError as err:
        print(err)
        return False
