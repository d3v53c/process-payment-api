from .base import *


class DevelopmentConfig(Config):
    """
    Development Configuration.
    """
    DEVELOPMENT = True
    DEBUG = True
    SERVER_MOCK = 'payment.server.json'

    # base api url
    BASE_URL = 'http://localhost:5000'