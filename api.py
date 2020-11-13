from core.view import APIView


class ProcessPayment(APIView):
    """
    Controller for the `ProcessPayment` API.
    Describes http method definitions.
    """

    def get(self, *args, **kwargs):
        return Response('ProcessPayment')