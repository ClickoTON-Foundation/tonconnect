class BaseRequestOption():
    def __init__(self):
        self.name = None
    
    def to_dict(self):
        return {'name': self.name}

class AddressRequestOption(BaseRequestOption):
    def __init__(self):
        self.name = 'ton_addr'

class ProofRequestOption(BaseRequestOption):
    def __init__(self, payload):
        self.name = 'ton_proof'
        self.payload = payload
    
    def to_dict(self):
        return {'name': self.name, 'payload': self.payload}
