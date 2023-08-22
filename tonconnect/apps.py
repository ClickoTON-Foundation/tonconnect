from .wallet import Wallet


class Tonkeeper(Wallet):
    def __init__(self, timeout: int=600):
        super().__init__('app.tonkeeper.com', 'bridge.tonapi.io/bridge', timeout)


class Tonhub(Wallet):
    def __init__(self, timeout: int=600):
        super().__init__('tonhub.com', 'connect.tonhubapi.com/tonconnect', timeout)


APPS = {
    'tonkeeper': Tonkeeper,
    'tonhub': Tonhub
}
