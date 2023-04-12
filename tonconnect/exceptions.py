class TONConnectException(BaseException):
    pass

class BridgeException(TONConnectException):
    pass

class ConnectorException(TONConnectException):
    pass
