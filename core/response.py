"""
Base Response class for all views.
"""


class Response(object):
    def __new__(
        cls,
        _dict,
        *args,
        status=None,
        error=False,
        message='',
        **kwargs,
    ):
        '''
        Returns a tuple of `(dictionary, status)` required by Flask API.
        '''

        if 'data' in _dict:
            _dict.update(success=not error)
            return _dict, status

        key = 'error' if error else 'data'

        return {
            'success': not error,
            'message': message,
            key: _dict,
        }, status