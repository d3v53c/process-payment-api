from flask.views import MethodView
from core.response import Response


class APIView(MethodView):
    '''
    APIView implementation in flask using MethodView.
    '''
    message = '{} method not allowed.'

    def get(self, *args, **kwargs):
        return Response(self.message.format('GET'))

    def post(self, *args, **kwargs):
        return Response(self.message.format('POST'))

    def put(self, *args, **kwargs):
        return Response(self.message.format('PUT'))

    def patch(self, *args, **kwargs):
        return Response(self.message.format('PATCH'))