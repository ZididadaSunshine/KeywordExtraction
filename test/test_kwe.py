import unittest
from flask import jsonify, json

from manage import app


class Test(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_connection(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_keyword_extraction(self):
        json_obj = json.dumps(dict(text='I really like this text! It is very nice'))

        response = self.app.post('/',
                                 data=json_obj,
                                 content_type='application/json',
                                 headers={'Authorization': 'anders'})

        response_json = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_json["keywords"] == ['like', 'text'] or
                        response_json["keywords"] == ['text', 'like'])

    def test_auth_failure(self):
        json_obj = json.dumps(dict(text='I really like this text! It is very nice'))

        response = self.app.post('/',
                                 data=json_obj,
                                 content_type='application/json',
                                 headers={'Authorization': 'incorrect'})

        self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
