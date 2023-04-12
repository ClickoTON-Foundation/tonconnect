from .wallet import Wallet


class Tonkeeper(Wallet):
    def __init__(self):
        super().__init__('app.tonkeeper.com', 'bridge.tonapi.io', '/bridge')


APPS = {
    'tonkeeper': Tonkeeper
}
