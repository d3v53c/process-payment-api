import unittest
import datetime as dt

from core.models import PaymentRequest


class PaymentRequestModelTest(unittest.TestCase):
    """
    TestCases for PaymentRequest model object.
    """
    def test_obj_initialisation(self):
        """
        TestCases for proper object initialization.
        """
        timestamp = dt.datetime.now() + dt.timedelta(minutes=1)
        data = dict(
            CreditCardNumber='1234567890123456',
            CardHolder='Tester',
            ExpirationDate=timestamp.isoformat(),
            SecurityCode='1234',
            Amount=100,
        )
        self.obj = PaymentRequest(**data)
        self.assertEqual(self.obj._creditCardNumber, '1234567890123456')
        self.assertEqual(self.obj._cardHolder, 'Tester')
        self.assertEqual(self.obj._expirationDate, timestamp.isoformat())
        self.assertEqual(self.obj._securityCode, '1234')
        self.assertEqual(self.obj._amount, 100)

        pm = self.obj.choose_payment_method()
        self.assertEqual(pm.get('gateway'), 'ExpensivePaymentGateway')

        self.obj.update_amount(15)
        pm = self.obj.choose_payment_method()
        self.assertEqual(pm.get('gateway'), 'CheapPaymentGateway')

        self.obj.update_amount(1500)
        pm = self.obj.choose_payment_method()
        self.assertEqual(pm.get('gateway'), 'PremiumPaymentGateway')

