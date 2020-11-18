import unittest
import json
import os

from core.api import MockApi
from core.tests import *
from app import app
from tests.test_api import ProcessPaymentTest

GATEWAYS = [
    'ExpensivePaymentGateway',
    'CheapPaymentGateway',
    'PremiumPaymentGateway',
]


class CheapPaymentGatewayTest(ProcessPaymentTest):
    """
    TestCase 1.
    This TestCase verifies if CheapPaymentGateway is not available,
    then server responds with a 500, and gateway timed out.
    It can be verified from the payment.server.json, only 1 attempt is made.

    ExpensivePaymentGateway - available
    CheapPaymentGateway - not available
    PremiumPaymentGateway - available
    Result:
    ExpensivePaymentGateway - attempts = 0
    CheapPaymentGateway - attempts = 1
    PremiumPaymentGateway - attempts = 0
    """
    def setUp(self):
        """
        Set CheapPaymentGateway as unavailable.
        """
        self.app = app.test_client()
        self.api = MockApi()
        self.api.reset()
        for gateway in GATEWAYS:
            if gateway == 'CheapPaymentGateway':
                item = self.api.put(
                    gateway,
                    'available',
                    0,
                )

    def tearDown(self):
        """
        Reset payment gateways all as available.
        """
        self.api.reset()

    def test_valid_data(self):
        # Given
        data = mock_valid_data()
        data["Amount"] = 10
        payload = json.dumps(data)

        # When
        response = self.app.post(
            '/process-payment',
            headers={"Content-Type": "application/json"},
            data=payload,
        )

        # Then
        self.assertEqual(500, response.status_code)
        self.assertEqual(False, response.json['success'])
        self.assertEqual(
            "CheapPaymentGateway timed out.",
            response.json['message'],
        )
        self.assertEqual(self.api.load()["CheapPaymentGateway"]["attempts"], 1)
        self.assertEqual(
            self.api.load()["ExpensivePaymentGateway"]["attempts"],
            0,
        )
        self.assertEqual(
            self.api.load()["PremiumPaymentGateway"]["attempts"],
            0,
        )


class ExpensivePaymentGatewayTest(ProcessPaymentTest):
    """
    TestCase 2.
    This TestCase verifies if ExpensivePaymentGateway is not available,
    then server tries CheapPaymentGateway 1 time,
    responds with a 200, if CheapPaymentGateway is available.
    It can be verified from the payment.server.json, only 1 attempt is made.

    ExpensivePaymentGateway - not available
    CheapPaymentGateway - available
    PremiumPaymentGateway - available
    Result:
    ExpensivePaymentGateway - attempts = 1
    CheapPaymentGateway - attempts = 1
    PremiumPaymentGateway - attempts = 0
    """
    def setUp(self):
        """
        Set ExpensivePaymentGateway as unavailable.
        """
        self.app = app.test_client()
        self.api = MockApi()
        self.api.reset()
        for gateway in GATEWAYS:
            if gateway == 'ExpensivePaymentGateway':
                item = self.api.put(
                    gateway,
                    'available',
                    0,
                )

    def tearDown(self):
        """
        Reset payment gateways all as available.
        """
        self.api.reset()

    def test_valid_data(self):
        # Given
        data = mock_valid_data()
        payload = json.dumps(data)

        # When
        response = self.app.post(
            '/process-payment',
            headers={"Content-Type": "application/json"},
            data=payload,
        )

        # Then
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, response.json['success'])
        self.assertEqual(
            "Payment is processed.",
            response.json['message'],
        )
        self.assertEqual(self.api.load()["CheapPaymentGateway"]["attempts"], 1)
        self.assertEqual(
            self.api.load()["ExpensivePaymentGateway"]["attempts"],
            1,
        )
        self.assertEqual(
            self.api.load()["PremiumPaymentGateway"]["attempts"],
            0,
        )


class ExpensiveAndCheapPaymentGatewayTest(ProcessPaymentTest):
    """
    TestCase 3.
    This TestCase verifies if ExpensivePaymentGateway is not available,
    then server tries CheapPaymentGateway 1 time,
    responds with a 500 and gateway timed out, if CheapPaymentGateway is not available.
    It can be verified from the payment.server.json, only 1 attempt for each gateway is made.

    ExpensivePaymentGateway - not available
    CheapPaymentGateway - available
    PremiumPaymentGateway - available
    Result:
    ExpensivePaymentGateway - attempts = 1
    CheapPaymentGateway - attempts = 1
    PremiumPaymentGateway - attempts = 0
    """
    def setUp(self):
        """
        Set ExpensivePaymentGateway as unavailable.
        """
        self.app = app.test_client()
        self.api = MockApi()
        self.api.reset()
        for gateway in GATEWAYS:
            if gateway == 'ExpensivePaymentGateway' or gateway == 'CheapPaymentGateway':
                item = self.api.put(
                    gateway,
                    'available',
                    0,
                )

    def tearDown(self):
        """
        Reset payment gateways all as available.
        """
        self.api.reset()

    def test_valid_data(self):
        # Given
        data = mock_valid_data()
        payload = json.dumps(data)

        # When
        response = self.app.post(
            '/process-payment',
            headers={"Content-Type": "application/json"},
            data=payload,
        )

        # Then
        self.assertEqual(500, response.status_code)
        self.assertEqual(False, response.json['success'])
        self.assertEqual(
            "CheapPaymentGateway timed out.",
            response.json['message'],
        )
        self.assertEqual(
            self.api.load()["ExpensivePaymentGateway"]["attempts"],
            1,
        )
        self.assertEqual(
            self.api.load()["PremiumPaymentGateway"]["attempts"],
            0,
        )
        self.assertEqual(self.api.load()["CheapPaymentGateway"]["attempts"], 1)

    def test_valid_data_without_security_code(self):
        # Given
        data = mock_valid_data_without_security_code()
        payload = json.dumps(data)

        # When
        response = self.app.post(
            '/process-payment',
            headers={"Content-Type": "application/json"},
            data=payload,
        )

        # Then
        self.assertEqual(500, response.status_code)
        self.assertEqual(False, response.json['success'])
        self.assertEqual(
            "CheapPaymentGateway timed out.",
            response.json['message'],
        )
        self.assertEqual(
            self.api.load()["ExpensivePaymentGateway"]["attempts"],
            1,
        )
        self.assertEqual(
            self.api.load()["PremiumPaymentGateway"]["attempts"],
            0,
        )
        self.assertEqual(self.api.load()["CheapPaymentGateway"]["attempts"], 1)


class PremiumPaymentGatewayTest(ProcessPaymentTest):
    """
    TestCase 1.
    ExpensivePaymentGateway - available
    CheapPaymentGateway - available
    PremiumPaymentGateway - not available
    Result:
    ExpensivePaymentGateway - attempts = 0
    CheapPaymentGateway - attempts = 0
    PremiumPaymentGateway - attempts = 3
    """
    def setUp(self):
        """
        Set PremiumPaymentGateway as unavailable.
        """
        self.app = app.test_client()
        self.api = MockApi()
        self.api.reset()
        for gateway in GATEWAYS:
            if gateway == 'PremiumPaymentGateway':
                item = self.api.put(
                    gateway,
                    'available',
                    0,
                )

    def tearDown(self):
        """
        Reset payment gateways all as available.
        """
        self.api.reset()

    def test_valid_data(self):
        # Given
        data = mock_valid_data()
        data["Amount"] = 1000
        payload = json.dumps(data)

        # When
        response = self.app.post(
            '/process-payment',
            headers={"Content-Type": "application/json"},
            data=payload,
        )

        # Then
        self.assertEqual(500, response.status_code)
        self.assertEqual(False, response.json['success'])
        self.assertEqual(
            "PremiumPaymentGateway timed out.",
            response.json['message'],
        )
        self.assertEqual(self.api.load()["CheapPaymentGateway"]["attempts"], 0)
        self.assertEqual(
            self.api.load()["ExpensivePaymentGateway"]["attempts"],
            0,
        )
        self.assertEqual(
            self.api.load()["PremiumPaymentGateway"]["attempts"],
            4,
        )
