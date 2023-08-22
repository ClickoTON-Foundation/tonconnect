import time
import json
import aiohttp
from .exceptions import BridgeException


class Client():
    def __init__(self, url):
        self.url = url
    
    async def get(self, timeout=60):
        async with aiohttp.ClientSession() as client:
            client: aiohttp.ClientSession
            response: aiohttp.StreamReader = (await client.get('https://' + self.url, headers={
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
                        try:
                            id = int(value)
                        except Exception:
                            id = int(value, base=16)

        return data, id
    
    async def send(self, body):
        async with aiohttp.ClientSession() as client:
            return await client.post('https://' + self.url, json=body)
