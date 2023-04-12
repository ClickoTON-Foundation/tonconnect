from nacl.public import PublicKey
from nacl.signing import VerifyKey

def public_key_from_hex(hex):
    return PublicKey(bytes.fromhex(hex))

def public_key_to_hex(public_key: PublicKey):
    return public_key.encode().hex()
