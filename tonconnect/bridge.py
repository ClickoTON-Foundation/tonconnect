import http.client
import requests
import base64
import json
from .crypto import SessionCrypto
from .utils import public_key_from_hex, public_key_to_hex
from .events import ConnectEvent
from .requests import Request


class Bridge():
    def __init__(self, url: str, slash_url: str = None):
        self.url = url
        self.slash_url = slash_url if slash_url is not None else ''
        self.session = None
        self.last_id = None
        self.ttl = 300
    
    def next_id(self):
        if self.last_id is None:
            return None
        else:
            self.last_id += 1
            return self.last_id
    
    def connect(self, session: SessionCrypto = None):
        if session is None:
            session = SessionCrypto()
        self.session = session
    
    def get_event(self):
        if self.session is None:
            return None

        url = f'{self.slash_url}/events?client_id={self.session.to_hex()}'
        if self.last_id is not None:
            url += f'&last_event_id={self.last_id}'
        
        connection = http.client.HTTPSConnection(self.url, 443)
        connection.request('GET', url, headers={
            'Accept': 'text/event-stream',
            'Connection': 'Keep-Alive',
        })
        
        with connection.getresponse() as response:
            run = True
            while run:
                for line in response:
                    line = line.decode('UTF-8')
                    if line == '\r\n':
                        break
                    if ':' in line and not line.startswith(':'):
                        key, value = line.split(':', 1)
                        value = value.strip()
                        if key == 'data':
                            data = json.loads(value)
                            run = False
                            break
                        elif key == 'id':
                            id = value
                        else:
                            print(key, value)
        
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

    def send_request(self, message: Request):
        if self.session is None:
            return None
        
        message = message.to_dict()
        print(message)
        encrypted_message = self.session.encrypt(json.dumps(message))
        print(encrypted_message)
        concatenated_message = b''.join([bytes(i) for i in encrypted_message])
        body = base64.b64encode(concatenated_message).decode()
        print(body)
        
        answer = requests.post(f'https://{self.url}{self.slash_url}/message?client_id={self.session.to_hex()}&to={public_key_to_hex(self.session.app_public_key)}&ttl={self.ttl}&topic={message["method"]}', data=body)
        print(answer.text, 'sended')
        
        return self.get_event()
