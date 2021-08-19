# refresh token 저장용으로 사용
import redis

class redisToken:
    def __init__(self):
        from os import getenv
        host = getenv("REDIS_HOST")
        port = getenv("REDIS_PORT")
        password=getenv("REDIS_PASSWD")
        db = 0 if getenv("REDIS_DB") is None else getenv("REDIS_DB")

        self.redisConn = redis.StrictRedis(host=host, port=port, db=db, password=password)
    
    def setRefreshToken(self, refreshToken, userID, UUID):
        try:
            # JWT Refresh Token
            self.redisConn.hset(refreshToken, "userID", userID)
            self.redisConn.hset(refreshToken, "UUID", UUID)
        except redis.RedisError() as err:
            print(err)
            # 레디스 에러나면 False 반환하고 
            # api 구현에서 500 반환
            return False
        
        # 인증 토큰은 api 응답에 보내야 해서 반환
        return True
    
    def getUserID(self, token):
        try:
            userID = self.redisConn.hget(token, "userID")
        except redis.RedisError as err:
            print(err)
            return False

        return userID

    def getUUID(self, token):
        try:
            UUID = self.redisConn.hget(token, "UUID")
        except redis.RedisError as err:
            print(err)
            return False
            
        return UUID