import unittest
import json
import datetime as dt

from app import app


DATE_TIME_ISO_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

class ProcessPaymentTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_expired_data(self):
        # Given
        payload = json.dumps({
            "CreditCardNumber": "123454567890123456",
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
        self.assertEqual(False, response.json['success'])
        self.assertEqual(400, response.status_code)

    def test_valid_data(self):
        # Given
        payload = json.dumps({
            "CreditCardNumber": "123454567890123456",
            "CardHolder": "Test Name",
            "ExpirationDate": (dt.datetime.now() + dt.timedelta(hours=1)).isoformat(),
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
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, response.json['success'])

    # def test

    def tearDown(self):
        pass