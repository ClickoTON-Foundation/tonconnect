from .crypto import SessionCrypto
from .static import Metadata
from .options import AddressRequestOption, ProofRequestOption
from .wallet import Wallet
from .bridge import Bridge, AsyncBridge
from .apps import APPS
from .exceptions import ConnectorException


class BaseConnector():
    def __init__(self, metadata: str):
        self.session = SessionCrypto()
        self.metadata_url = metadata
        self.metadata: Metadata = None
        self.wallet: Wallet = None
        self.bridge: Bridge = None
    
    def connect(self, wallet: str, payload: str):
        metadata = Metadata(self.metadata_url, [AddressRequestOption(), ProofRequestOption(payload)])
        
        if wallet not in APPS:
            raise ConnectorException(f'Unknown wallet {wallet}.')
        
        self.wallet = APPS[wallet]()
        self.bridge = self.wallet.bridge
        
        self.bridge.connect(self.session)
        return self.wallet.get_url(metadata)
    
    def check_address_proof_event(self, event):
        if event.address is None or event.proof is None:
            raise ConnectorException('Getting address without ton proof and ton address.')
        
        if not event.proof.check(event.address.raw_address, event.address.get_verify_key()):
            raise ConnectorException('Invalid proof.')
        
        return event.address.address
    
    def get_address(self) -> str:
        pass

class Connector(BaseConnector):
    def get_address(self):
        event = self.bridge.get_event()
        
        return self.check_address_proof_event(event)

class AsyncConnector(BaseConnector):
    async def connect(self, wallet: str, payload: str):
        metadata = Metadata(self.metadata_url, [AddressRequestOption(), ProofRequestOption(payload)])
        
        if wallet not in APPS:
            raise ConnectorException(f'Unknown wallet {wallet}.')
        
        self.wallet = APPS[wallet](bridge_client=AsyncBridge)
        self.bridge = self.wallet.bridge
        
        self.bridge.connect(self.session)
        return self.wallet.get_url(metadata)
    
    async def get_address(self):
        event = await self.wallet.bridge.get_event()
        
        return self.check_address_proof_event(event)
