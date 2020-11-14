import json
from flask_api import status
from flask import request
from marshmallow import ValidationError
from core.view import APIView
from core.response import Response
from core.schema import PaymentRequestSchema


class ProcessPayment(APIView):
    """
    Controller for the `ProcessPayment` API.
    Describes http method definitions.
    """
    def get(self, *args, **kwargs):
        return Response('ProcessPayment', status=200)

    def post(self, *args, **kwargs):
        """
        Http method: POST
        """
        data = request.data
        pr_schema = PaymentRequestSchema()
        try:
            payment_request = pr_schema.load(data)
            print(payment_request)
            processed_data, err = payment_request.process()
            if err:
                raise Exception(str(err))
        except ValidationError as e:
            print(e.messages)
            raise
            return Response(
                message='The request is invalid.',
                status=status.HTTP_400_BAD_REQUEST,
                error=True,
            )
        except Exception as unknown_err:
            raise
            return Response(
                message='Unknown error occured.',
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error=True,
            )
        return Response(status=status.HTTP_200_OK, message='Payment is processed.')