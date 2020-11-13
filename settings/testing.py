from .base import *


class TestingConfig(Config):
    """
    Testing Configuration.
    """
    TESTING = True

    # database connection
    SQLALCHEMY_DATABASE_URI = "sqlite://"