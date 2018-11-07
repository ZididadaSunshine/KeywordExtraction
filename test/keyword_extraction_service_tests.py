from unittest import main
from base import BaseTestCase
from app.main.service.kwe_service import extract_keywords


class KeywordExtractionServiceTest(BaseTestCase):
    def test_kwe_service_success(self):
        result = extract_keywords(dict(text='I really like this text! It is very nice'))

        self.assertEquals(result[1], 200)
        self.assertEquals(set(result[0]['keywords']), {'nice', 'text', 'really', 'like'})

    def test_kwe_service_error(self):
        result = extract_keywords(dict())

        self.assertEquals(result, 400)


if __name__ == "__main__":
    main()
