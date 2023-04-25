from .bridge import Bridge
from .wallet import Wallet


class Tonkeeper(Wallet):
    def __init__(self, bridge_client = Bridge):
        super().__init__('app.tonkeeper.com', 'bridge.tonapi.io', '/bridge', bridge_client)


APPS = {
    'tonkeeper': Tonkeeper
}
