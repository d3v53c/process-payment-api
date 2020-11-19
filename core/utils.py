import datetime as dt


def mock_expired_data():
    """
    Returns an expired test data.
    """
    return {
        "CreditCardNumber": "123454567890123456",
        "CardHolder": "Test",
        "ExpirationDate": "2014-12-22T03:12:58.019077+00:00",
        "SecurityCode": "1234",
        "Amount": 100
    }


def mock_invalid_credit_card_data():
    """
    Returns invalid credit card data.
    """
    return {
        "CreditCardNumber": "1234",
        "CardHolder": "Test Name",
        "ExpirationDate":
        (dt.datetime.now() + dt.timedelta(minutes=1)).isoformat(),
        "SecurityCode": "1234",
        "Amount": 100
    }


def mock_valid_data():
    """
    Returns valid data.
    """
    return {
        "CreditCardNumber": "123454567890123456",
        "CardHolder": "Test Name",
        "ExpirationDate":
        (dt.datetime.now() + dt.timedelta(hours=1)).isoformat(),
        "SecurityCode": "1234",
        "Amount": 100
    }


def mock_valid_data_without_security_code():
    """
    Returns valid data without security code.
    """
    return {
        "CreditCardNumber": "123454567890123456",
        "CardHolder": "Test Name",
        "ExpirationDate":
        (dt.datetime.now() + dt.timedelta(hours=1)).isoformat(),
        "Amount": 100
    }
