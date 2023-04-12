# WIP, this code isn't working

from tonconnect.connector import Connector
from tonconnect.requests import SendRequest, SendMessage
import time


connector = Connector('https://tonclick.online/ton-connect.json')
url = connector.connect('tonkeeper', 'test')

print(f'Universal connect url for Tonkeeper: {url}')

address = connector.get_address()
print(f'Successfuly connected {address}.')

request = SendRequest(connector.wallet.bridge.next_id(), [SendMessage('address', 1)], time.time() + 1000, -239, 'address')
connector.bridge.send_request(request)
