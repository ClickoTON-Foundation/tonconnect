from .crypto import SessionCrypto
from .static import Metadata
from .options import AddressRequestOption, ProofRequestOption
from .wallet import Wallet
from .bridge import Bridge
from .apps import APPS


class Connector():
    def __init__(self, metadata: str):
        self.session = SessionCrypto()
        self.metadata_url = metadata
        self.metadata: Metadata = None
        self.wallet: Wallet = None
        self.bridge: Bridge = None
    
    def connect(self, wallet: str, payload: str):
        metadata = Metadata(self.metadata_url, [AddressRequestOption(), ProofRequestOption(payload)])
        
        if wallet not in APPS:
            return None
        
        self.wallet = APPS[wallet]()
        self.bridge = self.wallet.bridge
        
        self.bridge.connect(self.session)
        return self.wallet.get_url(metadata)
    
    def get_address(self):
        event = self.bridge.get_event()
        
        if event.address is None or event.proof is None:
            return None
        
        if not event.proof.check(event.address.raw_address, event.address.get_verify_key()):
            return None
        
        return event.address.address
        