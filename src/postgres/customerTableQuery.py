import psycopg2 as db
# customer table

# 고객 명단 불러오기
def getCustomerDict(self, UUID):
    try:
        self.cur.execute("""
            SELECT customer_id,name,phone_number 
            FROM customer
            WHERE UUID = %s""",
            (UUID,))
        return dict(self.cur.fetchall())
    except db.DatabaseError as err:
        print(err)
        return None

def getCustomerInfo(self, userData):
    UUID = userData["UUID"]
    customerID = userData["customerID"]

    try:
        self.cur.execute("""
            SELECT name,phone_number 
            FROM customer
            WHERE UUID = %s AND customer_id = %s""",
            (UUID, customerID,))
        return dict(self.cur.fetchone())
    except db.DatabaseError as err:
        print(err)
        return None

# 새 고객 추가
def addNewCustomer(self, userData):
    UUID = userData["UUID"]
    customerID = userData["customerID"]
    name = userData["name"]
    phoneNumber = userData["phoneNumber"]

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
def getCustomerID(self, userData):
    UUID = userData["UUID"]
    name = userData["name"]
    phoneNumber = userData["phoneNumber"]

    try:
        self.cur.execute("""
            SELECT customer_id 
            FROM customer
            WHERE UUID = %s AND name = %s AND phone_number = %s""",
            (UUID, name, phoneNumber,))
        return dict(self.cur.fetchone())
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
        return True
    except db.DatabaseError as err:
        print(err)
        return False
