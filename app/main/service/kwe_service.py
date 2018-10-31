from app.keyword_graph import TKGExtractor


class KWEServiceResponse:
    Success = 200
    Error = 400


def extract_keywords(data):
    if not data or 'text' not in data:
        return KWEServiceResponse.Error
    else:
        extractor = TKGExtractor(data['text'].split('\n'))
        return dict(keywords=extractor.extract_n_keywords(n=15)), KWEServiceResponse.Success
