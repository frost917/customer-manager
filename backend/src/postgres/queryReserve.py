import psycopg2 as db

def getAllReserve(self, UUID):
    try:
        self.cur.execute("""
            SELECT 
                reserve_id
            FROM reserve
            WHERE user_id = uuid(%s) AND is_completed IS NOT TRUE""",
            (UUID,))

        result = self.cur.fetchall()
        if result is None:
            result = dict()
        return result

    except db.DatabaseError as err:
        print(err)
        return dict()

def getReserveData(self, reserveID):
    try:
        self.cur.execute("""
            SELECT 
                customer_id,
                reserve_time
            FROM reserve_data
            WHERE reserve_id = uuid(%s)""",
            (reserveID,))

        result = self.cur.fetchone()
        if result is None:
            result = dict()
        return result

    except db.DatabaseError as err:
        print(err)
        return dict()

def getReserveType(self, reserveID):
    try:
        self.cur.execute("""
            SELECT 
                reserve_type.type_id,
                job_type.job_name
            FROM reserve_type
            INNER JOIN job_type
            ON ( job_type.type_id = reserve_type.type_id )
            WHERE reserve_type.reserve_id = uuid(%s)""",
            (reserveID,))

        result = self.cur.fetchall()
        if result is None:
            result = dict()
        return result

    except db.DatabaseError as err:
        print(err)
        return dict()

def getReserveFromCustomerID(self, customerID):
    try:
        self.cur.execute("""
            SELECT 
                reserve_id,
                reserve_time
            FROM reserve_data
            WHERE customer_id = uuid(%s)""",
            (customerID,))

        result = self.cur.fetchall()
        if result is None:
            result = dict()
        return result

    except db.DatabaseError as err:
        print(err)
        return dict()

def addNewReserve(self, UUID, reserveData: dict):
    customerID = reserveData['customerID']
    reserveID = reserveData['reserveID']
    reserveTime = reserveData['reserveTime']
    reserveType = reserveData['reserveType']

    # 시술 기록 생성시 시술 타입이 리스트로 들어오기 때문에
    # 이거 하나하나 분리해서 시술할 필요가 있음
    try:
        self.cur.execute("""
        WITH data (
            user_id, customer_id, reserve_id, reserve_time
        ) AS ( VALUES ( 
			uuid(%s), uuid(%s), uuid(%s), to_timestamp(%s, 'YYYY-MM-DD HH24:MI') ) 
        ), create_reserve AS (
            INSERT INTO reserve ( user_id, reserve_id )
            SELECT user_id, reserve_id FROM data 
        )
        INSERT INTO reserve_data ( reserve_id, customer_id, reserve_time )
        SELECT reserve_id, customer_id, reserve_time FROM data""",
        (UUID, customerID, reserveID, reserveTime, ))

        for jobType in reserveType:
            self.cur.execute("""
            INSERT INTO reserve_type
            ( reserve_id, type_id )
            VALUES (
                uuid(%s), CAST( %s AS INTEGER )
            )""", 
            (reserveID, jobType,))

        self.dbconn.commit()
        return True
    except db.DatabaseError as err:
        print(err)
        return False

def updateReserve(self, reserveData):
    reserveID = reserveData['reserveID']
    reserveTime = reserveData['reserveTime']
    reserveType = reserveData['reserveType']

    try:
        self.cur.execute("""
        UPDATE
            reserve_data
        SET
            reserve_time = to_timestamp(%s, 'YYYY-MM-DD HH24:MI')
        WHERE reserve_id = uuid(%s)
        )""", 
        (reserveTime ,reserveID, ))

        self.cur.execute("""
        DELETE FROM reserve_type
        WHERE reserve_id = uuid(%s)
        """, (reserveID, ))

        for jobType in reserveType:
            self.cur.execute("""
            INSERT INTO reserve_type
                ( reserve_id, type_id )
            VALUES (
                uuid(%s), CAST( %s AS INTEGER ) 
            )""", (reserveID, jobType, ))
            
        self.dbconn.commit()
        return True
    except db.DatabaseError as err:
        print(err)
        return False

def deleteReserve(self, reserveID):
    try:
        self.cur.execute("""
        WITH data (
            reserve_id
            ) AS ( VALUES (uuid(%s) ) ),
            delete_reserve_type AS (
                DELETE FROM reserve_type
                WHERE reserve_id IN ( SELECT data.reserve_id FROM data )
            )
            delete_reserve_data AS (
                DELETE FROM reserve_type
                WHERE reserve_data IN ( SELECT data.reserve_id FROM data )
            )
            DELETE FROM reserve
            WHERE reserve_id IN ( SELECT data.reserve_id FROM data )
        )""", (reserveID, ))
        self.dbconn.commit()
        return True
    except db.DatabaseError as err:
        print(err)
        return False

def setReserveComplete(self):
    try:
        self.cur.execute("""
        UPDATE
            reserve
        SET
            reserve.is_completed IS TRUE
        WHERE 
            reserve_data.reserv_id = reserve.reserve_id 
            AND
            reserve_data.reserve_time < now()
        """)

        self.dbconn.commit()
        return True
    except db.DatabaseError as err:
        print(err)
        return False
    