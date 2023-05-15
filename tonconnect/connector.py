import aiohttp
import requests
from nacl.signing import VerifyKey
from .crypto import SessionCrypto
from .static import Metadata
from .options import AddressRequestOption, ProofRequestOption
from .wallet import Wallet
from .bridge import Bridge, AsyncBridge
from .apps import APPS
from .exceptions import ConnectorException
from .events import ConnectEvent


class Connector():
    def __init__(self, metadata: str, use_tonapi: bool = False, tonapi_token: str = None):
        self.session = SessionCrypto()
        self.metadata_url = metadata
        self.metadata: Metadata = None
        self.wallet: Wallet = None
        self.bridge: Bridge = None
        self.use_tonapi: bool = use_tonapi
        self.tonapi_token: str = tonapi_token
    
    def connect(self, wallet: str, payload: str):
        metadata = Metadata(self.metadata_url, [AddressRequestOption(), ProofRequestOption(payload)])
        
        if wallet not in APPS:
            raise ConnectorException(f'Unknown wallet {wallet}.')
        
        self.wallet = APPS[wallet]()
        self.bridge = self.wallet.bridge
        
        self.bridge.connect(self.session)
        return self.wallet.get_url(metadata)
    
    def get_address(self):
        event = self.bridge.get_event()
        
        return self.check_address_proof_event(event)
    
    def get_verify_key(self, address: str) -> str:
        result = requests.get(f'https://tonapi.io/v2/blockchain/accounts/{address}/methods/get_public_key', headers={'Authorization': self.tonapi_token})
        json = result.json()
        verify_key = VerifyKey(key=int(json['decoded']['public_key']).to_bytes(32, byteorder='big'))
        
        return verify_key
    
    def check_address_proof_event(self, event: ConnectEvent):
        if event.address is None or event.proof is None:
            raise ConnectorException('Getting address without ton proof and ton address.')
        
        if self.use_tonapi:
            verify_key = self.get_verify_key(event.address.address)
        else:
            verify_key = event.address.get_verify_key()
        
        if not event.proof.check(event.address.raw_address, verify_key):
            raise ConnectorException('Invalid proof.')
        
        return event.address.address

class AsyncConnector(Connector):
    async def connect(self, wallet: str, payload: str):
        metadata = Metadata(self.metadata_url, [AddressRequestOption(), ProofRequestOption(payload)])
        
        if wallet not in APPS:
            raise ConnectorException(f'Unknown wallet {wallet}.')
        
        self.wallet = APPS[wallet](bridge_client=AsyncBridge)
        self.bridge: AsyncBridge = self.wallet.bridge
        
        self.bridge.connect(self.session)
        return self.wallet.get_url(metadata)
    
    async def get_address(self):
        event = await self.bridge.get_event()
        
        return await self.check_address_proof_event(event)
    
    async def get_verify_key(self, address: str):
        async with aiohttp.ClientSession() as client:
            result = await client.get(f'https://tonapi.io/v2/blockchain/accounts/{address}/methods/get_public_key', headers={'Authorization': self.tonapi_token})
            json = await result.json()
            verify_key = VerifyKey(key=int(json['decoded']['public_key']).to_bytes(32, byteorder='big'))
        
        return verify_key

    async def check_address_proof_event(self, event: ConnectEvent):
        if event.address is None or event.proof is None:
            raise ConnectorException('Getting address without ton proof and ton address.')
        
        if self.use_tonapi:
            verify_key = await self.get_verify_key(event.address.address)
        else:
            verify_key = event.address.get_verify_key()
        
        if not event.proof.check(event.address.raw_address, verify_key):
            raise ConnectorException('Invalid proof.')
        
        return event.address.address
