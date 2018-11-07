from unittest import main
from base import BaseTestCase
from flask import json


class KeywordExtractionControllerTest(BaseTestCase):
    def setUp(self):
        self.test_client = self.app.test_client()

    def test_auth_success(self):
        response = self.test_client.post('/',
                                         data=json.dumps(dict(text='I really like this text! It is very nice')),
                                         content_type='application/json',
                                         headers={'Authorization': 'anders'})

        self.assert200(response)
        self.assertEquals(set(response.json['keywords']), {'nice', 'text', 'really', 'like'})

    def test_auth_invalid(self):
        response = self.test_client.post('/',
                                         data=json.dumps(dict(text='I really like this text! It is very nice')),
                                         content_type='application/json',
                                         headers={'Authorization': '...'})

        self.assert401(response)
        self.assertEquals(response.json, dict(message='Invalid API key'))

    def test_auth_none(self):
        response = self.test_client.post('/',
                                         data=json.dumps(dict(text='I really like this text! It is very nice')),
                                         content_type='application/json')

        self.assert401(response)
        self.assertEquals(response.json, dict(message='API key required'))


if __name__ == "__main__":
    main()
