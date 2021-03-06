# refresh token 저장용으로 사용
import redis

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            cls._instances[cls].__init__(*args, **kwargs)
 
        return cls._instances[cls]

class redisToken(metaclass=Singleton):
    def __init__(self):
        # from os import getenv
        from config.secret import redisData
        # host = getenv("REDIS_HOST") if getenv("REDIS_HOST") is not None else 'localhost'
        # port = getenv("REDIS_PORT") if getenv("REDIS_PORT") is not None else '6432'
        # password = getenv("REDIS_PASSWD") if getenv("REDIS_PASSWD") is not None else ''

        host = redisData.get("REDIS_HOST")
        port = redisData.get("REDIS_PORT")
        password = redisData.get("REDIS_PASSWD")
        db = 0

        pool = redis.ConnectionPool(max_connections=5,
            host=host,
            port=port, 
            db=db, 
            password=password,
            connection_class=redis.SSLConnection,
            ssl_cert_reqs='required',
            ssl_ca_certs='/certs/ca.crt',
            ssl_certfile='/certs/tls.crt',
            ssl_keyfile='/certs/tls.key')

        self.redisConn = redis.StrictRedis(connection_pool=pool)

    
    def __del__(self):
        self.redisConn.close()

    def setRefreshToken(self, refreshToken, userID, UUID):
        from datetime import timedelta
        # JWT Refresh Token
        try:
            self.redisConn.hset(refreshToken, "userID", userID)
            self.redisConn.hset(refreshToken, "UUID", UUID)
            self.redisConn.expire(refreshToken, timedelta(hours=720))
        except redis.RedisError as err:
            print(err)
            return False

        # 인증 토큰은 api 응답에 보내야 해서 반환
        return True
    
    def delRefreshToken(self, refreshToken):
        try:
            self.redisConn.delete(refreshToken)
        except redis.RedisError as err:
            print(err)
            # 레디스 에러나면 False 반환하고 
            # api 구현에서 500 반환
            return False

    def getUserID(self, refreshToken):
        try:
            userID = self.redisConn.hget(refreshToken, "userID")
        except redis.RedisError as err:
            print(err)
            return None

        if userID is not None:
            userID = userID.decode('utf-8')
        return userID

    def getUUID(self, refreshToken):
        try:
            UUID = self.redisConn.hget(refreshToken, "UUID")
        except redis.RedisError as err:
            print(err)
            return None

        if UUID is not None:
            UUID = UUID.decode('utf-8')
        return UUID
