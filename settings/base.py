import os

# root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config(object):
    """
    Base configuration object for the app.
    """

    # project version
    VERSION_NAME = 'mock-api'
    VERSION_NUMBER = '0.0.1'
    DEBUG = False
    TESTING = False
    SERVER_MOCK = None

    # base url where the server is hosted.
    BASE_URL = ''

    # SECURITY WARNING: Keep the key secret in production.
    SECRET_KEY = '+&i8*5iey3k*@4ej_s(r$t2gs-wioa_wnw_976uz+^xgx^hk*c'