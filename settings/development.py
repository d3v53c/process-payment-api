from .base import *


class DevelopmentConfig(Config):
    """
    Development Configuration.
    """
    DEVELOPMENT = True
    DEBUG = True

    # base api url
    BASE_URL = 'http://localhost:5000'

    os.environ.setdefault('AUTHLIB_INSECURE_TRANSPORT', 'True')