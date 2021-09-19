import os

JWTSecret = os.getenv('JWTSecret')

dbData = dict()
dbData['DB_HOST'] = os.getenv("DB_HOST")
dbData['DB_DATABASE'] = os.getenv("DB_DATABASE")
dbData['DB_PORT'] = os.getenv("DB_PORT")
dbData['DB_USER'] = os.getenv("DB_USER")
dbData['DB_PASSWD'] = os.getenv("DB_PASSWD")

redisData = dict()
redisData['REDIS_HOST']
redisData['REDIS_PORT']
redisData['REDIS_PASSWD']