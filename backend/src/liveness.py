from flask import Blueprint, Response

manager = Blueprint('liveness', __name__, url_prefix='/ping')

@manager.route('')
def isLive():
    return Response('pong!', status=200, content_type='html/text; charset=UTF-8')