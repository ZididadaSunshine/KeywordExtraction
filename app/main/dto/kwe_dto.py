from flask_restplus import fields, Namespace


class KWEDTO:
    api = Namespace('Keyword-Extraction', description='Keyword Extraction operations.')
    extract_keywords = api.model('Extract Keywords', {
                                 'text': fields.String(required=True, description='Text to get keywords from')})
