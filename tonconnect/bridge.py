import base64
import json
from .crypto import SessionCrypto
from .utils import public_key_from_hex, public_key_to_hex
from .events import ConnectEvent
from .requests import Request
from .exceptions import BridgeException
from .httpbridge import SyncClient, AsyncClient

class BaseBridge():
    def __init__(self, url: str, slash_url: str = None, ttl: int = 300, timeout: int = 600):
        self.url = url
        self.slash_url = slash_url if slash_url is not None else ''
        self.session = None
        self.last_id = None
        self.last_rpc_id = None
        self.ttl = ttl
        self.timeout = timeout
    
    def next_id(self):
        if self.last_rpc_id is None:
            self.last_rpc_id = 0
        else:
            self.last_rpc_id += 1
        return self.last_rpc_id
    
    def connect(self, session: SessionCrypto = None):
        if session is None:
            session = SessionCrypto()
        self.session = session
    
    def get_events_url(self):
        if self.session is None:
            raise BridgeException('Getting event on non-connected bridge.')

        url = f'{self.slash_url}/events?client_id={self.session.to_hex()}'
        if self.last_id is not None:
            url += f'&last_event_id={self.last_id}'
            
        return url
    
    def encode_event(self, data, id):
        encoded = base64.b64decode(data['message'])
        nonce = encoded[:24]
        message = encoded[24:]
        self.session.app_public_key = public_key_from_hex(data['from'])
        
        data = json.loads(self.session.decrypt(message, nonce))
        
        self.last_id = int(id)
        data['id'] = int(id)
        if data['event'] == 'connect':
            data = ConnectEvent.from_dict(data)
        
        return data

    def form_request(self, message: Request) -> tuple[str, str]:
        if self.session is None:
            raise BridgeException('Sending request on non-connected bridge.')
        
        message = message.to_dict()
        # print(json.dumps(message))
        encrypted_message = self.session.encrypt(json.dumps(message))
        # print(encrypted_message)
        concatenated_message = b''.join([bytes(i) for i in encrypted_message])
        body = base64.b64encode(concatenated_message).decode()
        # print(body)
        
        url = f'https://{self.url}{self.slash_url}/message?client_id={self.session.to_hex()}&to={public_key_to_hex(self.session.app_public_key)}&ttl={self.ttl}&topic={message["method"]}'
        
        return url, body

    def get_event(self) -> dict:
        return {}

    def send_request(self, message: Request) -> dict:
        return {}

class Bridge(BaseBridge):
    def get_event(self):
        url = self.get_events_url()
        
        client = SyncClient(self.url, url)
        data, id = client.get(self.timeout)
        
        return self.encode_event(data, id)
    
    def send_request(self, message: Request) -> dict:
        # WIP
        
        url, body = self.form_request(message)
        
        client = SyncClient(self.url, url)
        answer = client.send(body)
        # print(answer.text, 'sended')
        
        return self.get_event()

class AsyncBridge(BaseBridge):
    async def get_event(self):
        url = self.get_events_url()
        
        client = AsyncClient(self.url, url)
        data, id = await client.get(self.timeout)
        
        return self.encode_event(data, id)
    
    async def send_request(self, message: Request) -> dict:
        # WIP
        
        url, body = self.form_request(message)
        
        client = SyncClient(self.url, url)
        answer = await client.send(body)
        # print(answer.text, 'sended')
        
        return await self.get_event()
