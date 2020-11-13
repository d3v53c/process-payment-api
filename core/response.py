from flask_api import status


class Response(object):
    def __new__(
        cls,
        *args,
        status=status.HTTP_400_BAD_REQUEST,
        error=False,
        message='',
        **kwargs,
    ):
        '''
        Returns a tuple of `(dictionary, status)` required by Flask API.
        '''
        data = dict()
        if len(args) > 0 and isinstance(args[0], dict):
            data = args[0]

        if 'data' in data:
            data.update(success=not error)
            return data, status

        key = 'error' if error else 'data'

        return {
            'success': not error,
            'message': message,
            key: data,
        }, status