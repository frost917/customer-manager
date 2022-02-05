from flask import Response, make_response, redirect, render_template

from login.responseEnum import ResponseType
from datetime import datetime
from dateutil.relativedelta import relativedelta

def buildResponse(responseType: ResponseType, **kargs) -> Response:
    if responseType == ResponseType.LOGIN:
        accessToken = kargs.get('accessToken')
        refreshToken = kargs.get('refreshToken')
        tokenTime = kargs.get('tokenTime')

        response = make_response(redirect('/'))
        response.set_cookie('accessToken', accessToken, 
            expires=datetime.strptime(tokenTime, '%Y-%m-%d %H:%M:%S.%f') + relativedelta(hours=6), 
            secure=True, httponly=True)
        response.set_cookie('refreshToken', refreshToken, 
        expires=datetime.strptime(tokenTime, '%Y-%m-%d %H:%M:%S.%f') + relativedelta(months=6), 
        secure=True, httponly=True)
    
    elif responseType == ResponseType.LOGOUT:
        response = make_response(redirect('/login'))
        response.delete_cookie('accessToken', secure=True, httponly=True)
        response.delete_cookie('refreshToken', secure=True, httponly=True)

    elif responseType == ResponseType.TOKENEXPIRE:
        response = make_response(redirect('/login'))

    elif responseType == ResponseType.REFRESH:
        accessToken = kargs.get('accessToken')
        refreshToken = kargs.get('refreshToken')
        tokenTime = kargs.get('tokenTime')

        response = make_response("""<script>location.reload();</script>""")
        response.set_cookie('accessToken', accessToken, 
            expires=datetime.strptime(tokenTime, '%Y-%m-%d %H:%M:%S.%f') + relativedelta(hours=6), 
            secure=True, httponly=True)
        response.set_cookie('refreshToken', refreshToken, 
        expires=datetime.strptime(tokenTime, '%Y-%m-%d %H:%M:%S.%f') + relativedelta(months=6), 
        secure=True, httponly=True)

    elif responseType == ResponseType.ADDCUSTOMERS:
        customerID = kargs.get("customerID")

        response = make_response(redirect('/customers/' + customerID + '/jobs'))

    elif responseType == ResponseType.GETCUSTOMERS:
        customerID = kargs.get('customerID')
        customerData = kargs.get('customerData')
        jobData = kargs.get('jobData')

        response = make_response(
            render_template('customer-data.html', customerData=customerData, customerID=customerID, jobData=jobData)
            )

    elif responseType == ResponseType.ADDJOBS:
        customerData = kargs.get('customerData')
        customerID = kargs.get('customerID')
        
        response = make_response(render_template('job-add.html', customerData=customerData, customerID=customerID))

    elif responseType == ResponseType.GETJOBS:
        customerData = kargs.get('customerData')
        customerID = kargs.get('customerID')
        jobData = kargs.get('jobData')

        response = make_response(render_template('job-data.html', customerData=customerData, jobData=jobData, customerID=customerID))

    elif responseType == ResponseType.ERROR:
        response = make_response("""<script>
        alert("서버 에러");
        history.back();
        </script>""")

    elif responseType == ResponseType.ACCOUNTERROR:
        response = make_response("""<script>
            alert("아이디 또는 비밀번호가 잘못되었습니다");
            location.href="/login";
            </script>""")

    return response