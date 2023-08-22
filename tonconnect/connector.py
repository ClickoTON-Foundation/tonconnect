import aiohttp
from nacl.signing import VerifyKey
from .crypto import SessionCrypto
from .metadata import Metadata
from .options import AddressRequestOption, ProofRequestOption
from .wallet import Wallet
from .bridge import Bridge
from .apps import APPS
from .exceptions import ConnectorException
from .events import ConnectEvent
import asyncio
import base64


class AsyncConnector():
    def __init__(self, metadata: str, use_tonapi: bool = False, tonapi_token: str = None):
        self.session = SessionCrypto()
        self.metadata_url = metadata
        self.metadata: Metadata = None
        self.wallet: Wallet = None
        self.bridge: Bridge = None
        self.use_tonapi: bool = use_tonapi
        self.tonapi_token: str = tonapi_token
    
    async def connect(self, wallet: Wallet, payload: str, timeout: int=600) -> str:
        metadata = Metadata(self.metadata_url, [AddressRequestOption(), ProofRequestOption(payload)])
        
        if isinstance(wallet, str):
            if wallet not in APPS:
                raise ConnectorException(f'Unknown wallet {wallet}.')
            
            wallet = APPS[wallet]
        
        self.wallet: Wallet = wallet(timeout=timeout)
        self.bridge: Bridge = self.wallet.bridge
        
        await self.bridge.connect(self.session)
        return await self.wallet.get_url(metadata)
    
    async def get_address(self) -> str:
        event = await self.bridge.get_event()
        
        return await self.check_address_proof_event(event)
    
    async def get_verify_key(self, state_init: bytes) -> VerifyKey:
        async with aiohttp.ClientSession() as client:
            if self.tonapi_token is None:
                headers = {}
            else:
                headers = {'Authorization': self.tonapi_token}
            
            encoded = base64.b64encode(state_init).decode()
            result = await client.post(f'https://tonapi.io/v2/tonconnect/stateinit', json={'state_init': encoded}, headers=headers)
            json = await result.json()
            public_key = bytes.fromhex(json['public_key'])
            
            verify_key = VerifyKey(key=public_key)
        
        return verify_key

    async def check_address_proof_event(self, event: ConnectEvent) -> str:
        if event.address is None or event.proof is None:
            raise ConnectorException('Getting address without ton proof and ton address.')
        
        if self.use_tonapi:
            verify_key = await self.get_verify_key(event.address.state_init)
        else:
            verify_key = event.address.get_verify_key()
        
        if not event.proof.check(event.address.raw_address, verify_key):
            raise ConnectorException('Invalid proof.')
        
        return event.address.address


class Connector():
    def __init__(self, metadata: str, use_tonapi: bool = False, tonapi_token: str = None):
        self.async_connector = AsyncConnector(metadata, use_tonapi, tonapi_token)
    
    def connect(self, wallet: Wallet, payload: str, timeout: int=600) -> str:
        return asyncio.run(self.async_connector.connect(wallet, payload, timeout))
    
    def get_address(self) -> str:
        return asyncio.run(self.async_connector.get_address())
    
    def get_verify_key(self, address: str) -> str:
        return asyncio.run(self.async_connector.get_verify_key(address))
    
    def check_address_proof_event(self, event: ConnectEvent) -> str:
        return asyncio.run(self.async_connector.check_address_proof_event(event))
