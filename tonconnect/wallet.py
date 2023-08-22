from .bridge import Bridge
from .url import get_url
from .metadata import Metadata


class Wallet():
    def __init__(self, app: str, bridge: str, timeout: int=600):
        self.app = app
        self.bridge = Bridge(bridge, timeout=timeout)
    
    async def get_url(self, metadata: Metadata):
        return get_url(self.app, self.bridge.session.to_hex(), metadata)
