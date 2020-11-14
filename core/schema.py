from marshmallow import Schema, fields, post_load
from core.models import PaymentRequest


class PaymentRequestSchema(Schema):
    """
    Serializer schema for validating incoming request.
    """
    CreditCardNumber = fields.Str(required=True)
    CardHolder = fields.Str(required=True)
    ExpirationDate = fields.DateTime(required=True)
    SecurityCode = fields.Str()
    Amount = fields.Int(required=True)

    @post_load
    def make_request(self, data, **kwargs):
        return PaymentRequest(**data)