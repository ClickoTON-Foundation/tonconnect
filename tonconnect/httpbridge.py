import http.client
import time
import json
import requests
import aiohttp
from .exceptions import BridgeException


class SyncClient():
    def __init__(self, base_url, url):
        self.base_url = base_url
        self.url = url
    
    def get(self, timeout=60):
        connection = http.client.HTTPSConnection(self.base_url, 443)
        connection.request('GET', self.url, headers={
            'Accept': 'text/event-stream',
            'Connection': 'Keep-Alive',
        })
        
        start = time.time()
        with connection.getresponse() as response:
            run = True
            while run:
                for line in response:
                    if time.time() - start >= timeout:
                        raise BridgeException('Timeout while waiting for event.')
                    
                    line = line.decode('UTF-8')
                    if line == '\r\n':
                        run = False
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

        return data, id
    
    def send(self, body):
        return requests.post(self.base_url + self.url, data=body)

class AsyncClient():
    def __init__(self, base_url, url):
        self.base_url = base_url
        self.url = url
    
    async def get(self, timeout=60):
        async with aiohttp.ClientSession() as client:
            client: aiohttp.ClientSession
            response: aiohttp.StreamReader = (await client.get('https://' + self.base_url + self.url, headers={
                'Accept': 'text/event-stream',
                'Connection': 'Keep-Alive',
            })).content
            
            start = time.time()
            run = True
            while run:
                line: bytes = await response.readline()
                    
                if time.time() - start >= timeout:
                    raise BridgeException('Timeout while waiting for event.')
                
                line = line.decode('UTF-8')
                if line == '\r\n':
                    run = False
                    break
                if ':' in line and not line.startswith(':'):
                    key, value = line.split(':', 1)
                    value = value.strip()
                    if key == 'data':
                        data = json.loads(value)
                        run = False
                        break
                    elif key == 'id':
                        id = int(value)

        return data, id
    
    async def send(self, body):
        # WIP
        
        return None
