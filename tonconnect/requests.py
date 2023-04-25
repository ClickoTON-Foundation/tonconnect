import json


class Request():
    def __init__(self, method: str, id: int):
        self.method = method
        self.id = id
    
    def get_params(self):
        return {}
    
    def to_dict(self):
        params = self.get_params()
        
        result = {'method': self.method, 'params': params, 'id': self.id}
        return result

class SendMessage():
    def __init__(self, address: str, amount: int, payload: str = None, state_init: str = None):
        self.address = address
        self.amount = round(amount * (10 ** 9))
        self.payload = payload
        self.state_init = state_init
    
    def to_dict(self):
        result = {'address': self.address, 'amount': str(self.amount)}
        
        if self.payload is not None:
            result['payload'] = self.payload
        if self.state_init is not None:
            result['stateInit'] = self.state_init
        
        return result

class SendRequest(Request):
    def __init__(self, id: int, messages: list[SendMessage], valid_until: int = None, network: int = None, from_address: str = None):
        super().__init__('sendTransaction', id)
        
        self.valid_until = round(valid_until) * 1000
        self.network = network
        self.from_address = from_address
        self.messages = messages
    
    def get_params(self):
        params = {'messages': [message.to_dict() for message in self.messages]}
        
        if self.valid_until is not None:
            params['valid_until'] = self.valid_until
        if self.network is not None:
            params['network'] = str(self.network)
        if self.from_address is not None:
            params['from'] = self.from_address
        
        return [json.dumps(params)]
