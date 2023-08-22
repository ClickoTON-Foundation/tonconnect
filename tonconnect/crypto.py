import nacl.utils
from nacl.public import PublicKey, PrivateKey, Box


class SessionCrypto():
    def __init__(self, private_key: PrivateKey = None, app_public_key: PublicKey = None):
        if private_key is None:
            private_key = PrivateKey.generate()
        
        self.private_key = private_key
        self.app_public_key: PublicKey = app_public_key
        self.session_id: str = private_key.public_key.encode()
        
    def create_nonce(self) -> bytes:
        return nacl.utils.random(Box.NONCE_SIZE)
    
    def to_hex(self) -> str:
        return bytes(self.private_key.public_key).hex()
    
    def encrypt(self, message: str) -> tuple[bytes, nacl.utils.EncryptedMessage]:
        encoded_message = message.encode('utf-8')
        nonce = self.create_nonce()
        
        box = Box(self.private_key, self.app_public_key)
        encrypted = box.encrypt(encoded_message, nonce)
        
        return nonce, encrypted
    
    def decrypt(self, message: nacl.utils.EncryptedMessage, nonce: bytes) -> str:
        box = Box(self.private_key, self.app_public_key)
        decrypted = box.decrypt(message, nonce)
        
        return decrypted.decode()
