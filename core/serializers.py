from marshmallow import Schema, fields


class PaymentRequestScheme(Schema):
    """
    Serializer schema for validating incoming request.
    """
    CreditCardNumber = fields.Str(required=True)
    CardHolder = fields.Str(required=True)
    ExpirationDate = fields.DateTime(required=True)
    SecurityCode = fields.Str()
    Amount = fields.Int(required=True)