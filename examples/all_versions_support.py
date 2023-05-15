from tonconnect.connector import Connector


connector = Connector('https://tonclick.online/ton-connect.json', use_tonapi=True, tonapi_token=None)
url = connector.connect('tonkeeper', 'test')

print(f'Universal connect url for Tonkeeper: {url}')

address = connector.get_address()
print(f'Successfuly connected {address}.')
