import unittest
import json
import datetime as dt

from app import app
from core.utils import *
from core.api import MockApi

DATE_TIME_ISO_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


class ProcessPaymentApiTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.api = MockApi()
        self.api.reset()

    def test_expired_data(self):
        # Given
        payload = json.dumps(mock_expired_data())

        # When
        response = self.app.post(
            '/process-payment',
            headers={"Content-Type": "application/json"},
            data=payload,
        )

        # Then
        self.assertEqual(False, response.json['success'])
        self.assertEqual(400, response.status_code)

    def test_invalid_credit_card_data(self):
        # Given
        payload = json.dumps(mock_invalid_credit_card_data())

        # When
        response = self.app.post(
            '/process-payment',
            headers={"Content-Type": "application/json"},
            data=payload,
        )

        # Then
        self.assertEqual(400, response.status_code)
        self.assertEqual(False, response.json['success'])

    def test_valid_data(self):
        # Given
        payload = json.dumps(mock_valid_data())

        # When
        response = self.app.post(
            '/process-payment',
            headers={"Content-Type": "application/json"},
            data=payload,
        )

        # Then
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, response.json['success'])
        self.assertEqual("Payment is processed.", response.json['message'])

    def test_valid_data_without_security_code(self):
        # Given
        payload = json.dumps(mock_valid_data_without_security_code())

        # When
        response = self.app.post(
            '/process-payment',
            headers={"Content-Type": "application/json"},
            data=payload,
        )

        # Then
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, response.json['success'])
        self.assertEqual("Payment is processed.", response.json['message'])

    # def test

    def tearDown(self):
        self.api.reset()
