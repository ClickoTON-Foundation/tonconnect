from .bridge import Bridge
from .url import get_url
from .static import Metadata


class Wallet():
    def __init__(self, app: str, bridge: str, slash_url: str = None):
        self.app = app
        self.bridge = Bridge(bridge, slash_url)
    
    def get_url(self, metadata: Metadata):
        return get_url(self.app, self.bridge.session.to_hex(), metadata)
