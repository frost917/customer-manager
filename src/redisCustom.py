# maybe deprecated
import redis

class redisToken:
    def __init__(self):
        from os import getenv
        host = getenv("REDIS_HOST")
        port = getenv("REDIS_PORT")
        password=getenv("REDIS_PASSWD")
        db = 0 if getenv("REDIS_PORT") is None else getenv("REDIS_PORT")

        self.redisConn = redis.StrictRedis(host=host,
        port=port,
        db=db,
        password=password)
    
    def setToken(self, userID, UUID):
        from os import urandom
        from binascii import hexlify
        try:
            # 16자리 토큰은 랜덤 생성
            ## 나중에 jwt로 교체할 것 ##
            # DB에서 긁어온 id와 UUID는 hash로 저장
            token = hexlify(urandom(16))
            self.redisConn.hset(token, "userID", userID)
            self.redisConn.hset(token, "UUID", UUID)

        except redis.RedisError() as err:
            print(err)
            # 레디스 에러나면 False 반환하고 
            # api 구현에서 500 반환
            return False
        
        # 인증 토큰은 api 응답에 보내야 해서 반환
        return token
    
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