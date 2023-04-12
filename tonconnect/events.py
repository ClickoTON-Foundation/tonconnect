from dataclasses import dataclass
from ctypes import c_int32, c_int64
import hashlib
import base64
import tonsdk.utils
import nacl.signing
import nacl.public

@dataclass
class Address:
    raw_address: str
    address: str
    state_init: bytes
    
    def from_dict(data: dict):
        return Address(data['address'], tonsdk.utils.Address(data['address']).to_string(True, True, True, False), base64.b64decode(data['walletStateInit']))

    def get_key(self):
        state = self.state_init
        state = state[:-5]
        state = state[-32:]
        
        return state
    
    def get_verify_key(self):
        return nacl.signing.VerifyKey(self.get_key())


@dataclass
class AddressProof:
    timestamp: int
    domain_length: int
    domain: str
    payload: str
    signature: bytes
    
    def from_dict(data: dict):
        data = data['proof']
        
        signature = base64.b64decode(data['signature'])
        return AddressProof(data['timestamp'], data['domain']['lengthBytes'], data['domain']['value'], data['payload'], signature)
    
    def construct_message(self, address: str) -> bytes:
        address_data = tonsdk.utils._address.parse_friendly_address(tonsdk.utils.Address(address).to_string(True))
        address_hash = address_data['hash_part']
        
        wc = c_int32(address_data['workchain'])
        dl = c_int32(self.domain_length)
        ts = c_int64(self.timestamp)
        
        message = []
        message.append('ton-proof-item-v2/'.encode())
        message.append(bytes(wc))
        message.append(bytes(address_hash))
        message.append(bytes(dl))
        message.append(self.domain.encode())
        message.append(bytes(ts))
        message.append(self.payload.encode())
        
        message = b''.join(message)
        hashed_message = hashlib.sha256(message).hexdigest()
        
        full_message = []
        full_message.append(bytes.fromhex('ffff'))
        full_message.append('ton-connect'.encode())
        full_message.append(bytes.fromhex(hashed_message))
        full_message = b''.join(full_message)
        full_message = bytes.fromhex(hashlib.sha256(full_message).hexdigest())
        
        return full_message
    
    def check(self, address: str, public_key: nacl.signing.VerifyKey):
        message = self.construct_message(address)
        
        try:
            public_key.verify(message, self.signature)
                
            return True
        except Exception:
            return False

@dataclass
class Device:
    platform: str
    app: str
    version: str
    
    def from_dict(data: dict):
        return Device(data['platform'], data['appName'], data['appVersion'])

class ConnectEvent():
    def __init__(self, id: int, address: Address, proof: AddressProof, device: Device):
        self.id = id
        self.address: Address = address
        self.proof: AddressProof = proof
        self.device: Device = device
    
    def from_dict(data: dict):
        payload = data['payload']
        
        address = None
        proof = None
        device = None
        for item in payload['items']:
            if item['name'] == 'ton_addr':
                address = Address.from_dict(item)
            elif item['name'] == 'ton_proof':
                proof = AddressProof.from_dict(item)
        device = Device.from_dict(payload['device'])
        
        return ConnectEvent(int(data['id']), address, proof, device)
