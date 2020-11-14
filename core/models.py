import datetime as dt


class PaymentRequest:
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

    def choose_payment_method(self):
        """
        """
        payment_methods = self.get_payment_methods()
        gateway = dict(payment_id='cheap', **payment_methods.get('cheap'))
        if self._amount > 20:
            gateway = dict(
                payment_id='expensive',
                **payment_methods.get('expensive'),
            )
        if self._amount > 500:
            gateway = dict(
                payment_id='premium',
                **payment_methods.get('premium'),
            )
        return gateway

    def get_payment_methods(self):
        """
        Payment Methods available.
        Simple representation, these could be each an entire module in real life.
        """
        return dict(
            cheap=dict(
                gateway='CheapPaymentGateway',
                retry=0,
                strict=True,
                tier=1,
            ),
            expensive=dict(
                gateway='ExpensivePaymentGateway',
                retry=1,
                strict=False,
                tier=2,
            ),
            premium=dict(
                gateway='PremiumPaymentGateway',
                retry=3,
                strict=True,
                tier=3,
            ),
        )

    def process(self):
        """
        Process the payment request.
        Run pre-process checks.
        """
        try:
            payment_method = self.choose_payment_method()
            response, err = self.make_payment(**payment_method)
            if err:
                raise err
        except Exception as e:
            return None, e
        return response, None

    def make_payment(
        self,
        gateway=None,
        retry=0,
        strict=True,
        payment_id=None,
        **kwargs,
    ):
        """
        Here's where actually the payment is made.
        """
        while retry is not None and retry > -1:
            print(
                f"Loop start Gateway: {gateway}, Retry: {retry}, Strict: {strict}, Payment id: {payment_id}"
            )
            if gateway is None or payment_id is None:
                raise Exception(
                    "Internal Server error. Invalid payment gateway.")
            try:
                # make payment code here.
                # something fishy
                # payment_response = some_api.call()
                # return payment_response
                if gateway == 'ExpensivePaymentGateway':
                    raise Exception('Retry this madafaka')
                return dict(transaction_id='test'), None
            except Exception as e:
                print(
                    f"Error: {str(e)} Retry: {retry} PaymentID: {payment_id} -------------------------0> make_payment"
                )
                if strict:
                    print(f"Strict: {strict}")
                    continue
                payment_method = self.get_lower_tier_payment_method(payment_id)
                print(
                    f"Payment Method: {payment_method} -------------------------0> make_payment"
                )
                if payment_method:
                    gateway = payment_method.get('gateway')
                    payment_id = payment_method.get('payment_id')
                    strict = payment_method.get('strict')
                    retry = payment_method.get('retry')
                    print(f"Retry: {retry}")
                else:
                    retry -= 1
            else:
                return None, Exception('Payment gateway timed out.')

    def get_lower_tier_payment_method(self, identifier):
        """
        Retrieves a lower tier payment method available,
        if one is unavailable at the moment.
        """
        print(f"ID: {identifier} -0> get_lower_tier_payment_method")
        tier = self.get_tier_of_payment_method(identifier)
        print(f"Tier: {tier} -0> get_lower_tier_payment_method")
        while tier:
            tier -= 1
            payment_id = self.get_payment_method_by_tier(tier)
            if payment_id is not None:
                break
            if tier < 0:
                tier = None
        if payment_id is not None:
            return self.get_payment_method_by_id(payment_id)
        return

    def get_payment_method_by_id(self, identifier):
        """
        Retrieves a Payment method details by ID.
        """
        return dict(
            payment_id=identifier,
            **self.get_payment_methods().get(identifier, None),
        )

    def get_payment_method_tiers(self):
        """
        Retrieves a list of payment methods identifier sorted by their index,
        with tiers.
        """
        payment_methods = self.get_payment_methods()
        print(
            f"Payment Methods: {payment_methods} -------------------------0> get_payment_method_tiers"
        )
        res = list(
            map(
                lambda method: method['payment_id'],
                list(
                    sorted(map(
                        lambda data: dict(payment_id=data[0], **data[1]),
                        payment_methods.items()),
                           key=lambda item: item.get('tier', 0)))))
        print(f"Res: {res} -------------------")
        return res

    def get_tier_of_payment_method(self, identifier):
        """
        Retrieves a tier of a particular payment method using identifier.
        """
        print(f"Identifier: {identifier} -0> get_tier_of_payment_method")
        tiers = self.get_payment_method_tiers()
        print(
            f"Tiers: {tiers} -------------------------0> get_tier_of_payment_method"
        )
        return tiers.index(identifier) + 1

    def get_payment_method_by_tier(self, tier):
        """
        Retrieves a payment method by its tier. 
        """
        try:
            methods_by_tiers = self.get_payment_method_tiers()
            print(
                f"Methods by Tiers: {methods_by_tiers} ======================> get_payment_method_by_tier"
            )
            print(
                f"Tier: {tier} ======================> get_payment_method_by_tier"
            )
            return methods_by_tiers[tier - 1]
        except IndexError:
            return None
