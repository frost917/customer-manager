# from functools import wraps
# from datetime import timedelta

# from flask import g, make_response

# def makeResponse(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         template = func(*args, **kwargs)

#         accessToken = g.get('accessToken')
#         refreshToken = g.get('refreshToken')

#         result = make_response(template).
#         result.set_cookie('accessToken', accessToken, max_age=timedelta(hours=3), httponly=True)
#         result.set_cookie('refreshToken', refreshToken, max_age=timedelta(hours=4320), httponly=True)
#         return result

#     return wrapper