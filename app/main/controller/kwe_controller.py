from flask import request
from flask_restplus import Resource

from app.main.dto.kwe_dto import KWEDTO
from app.main.service.kwe_service import KWEServiceResponse, extract_keywords

api = KWEDTO.api


@api.route('')
class KWEResource(Resource):
    @api.response(KWEServiceResponse.Success, 'Successfully extracted keywords')
    @api.response(KWEServiceResponse.Error, 'An error occurred')
    @api.doc('Extract Keywords')
    @api.expect(KWEDTO.extract_keywords, validate=True)
    def post(self):
        return extract_keywords(request.json)
