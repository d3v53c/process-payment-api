import unittest
import json

from app import app


class SignupTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_successful_signup(self):
        # Given
        payload = json.dumps({
            "CreditCardNumber": "12345456",
            "CardHolder": "Test",
            "ExpirationDate": "2014-12-22T03:12:58.019077+00:00",
            "SecurityCode": "1234",
            "Amount": 100
        })

        # When
        response = self.app.post(
            '/process-payment',
            headers={"Content-Type": "application/json"},
            data=payload,
        )

        # Then
        self.assertEqual(True, response.json['success'])
        self.assertEqual(200, response.status_code)

    def tearDown(self):
        pass