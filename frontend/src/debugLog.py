from functools import wraps

# 토큰 살아있는지 확인
def pageLog(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(func.__name__)
        return func(*args, **kwargs)
    return wrapper