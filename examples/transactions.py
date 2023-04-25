# WIP, this code isn't working

from tonconnect.connector import Connector
from tonconnect.requests import SendRequest, SendMessage
import time


connector = Connector('https://tonclick.online/ton-connect.json')
url = connector.connect('tonkeeper', 'test')

print(f'Universal connect url for Tonkeeper: {url}')

address = connector.get_address()
print(f'Successfuly connected {address}.')

request = SendRequest(connector.wallet.bridge.next_id(), [SendMessage('0:0000000000000000000000000000000000000000000000000000000000000000', 0.000000001), SendMessage('0:0000000000000000000000000000000000000000000000000000000000000000', 0.000000001)], time.time() + 900, -239, '0:a0a61c7cad32343ee9309a0a55aa23e0aa0b93ba3850b1c83687b8e0738534b7')
print(connector.bridge.send_request(request))
