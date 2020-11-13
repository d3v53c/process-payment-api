import datetime as dt


class PaymentRequest(object):
    """
    Object holding payment request info.
    """

    def __init__(self, *args, **kwargs):
        self._creditCardNumber = kwargs.pop('CreditCardNumber', None)
        self._cardHolder = kwargs.pop('CardHolder', None)
        self._expirationDate = dt.datetime.now()
        self._securityCode = kwargs.pop('SecurityCode', None)
        self._amount = kwargs.pop('Amount', None)
        return

    def process(self):
        """
        Process the payment request.
        Run pre-process checks.
        """
        pass