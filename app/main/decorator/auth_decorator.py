from flask import request
from app.main.dto.kwe_dto import KWEDTO

api = KWEDTO.api


def auth_required(func):
    func = api.doc(security='key')(func)

    def check_auth(*args, **kwargs):
        if 'Authorization' not in request.headers:
            api.abort(401, 'API key required')
        key = request.headers['Authorization']

        # Check key validity
        if key != "anders":
            api.abort(401, 'Invalid API key')

        return func(*args, **kwargs)
    return check_auth
