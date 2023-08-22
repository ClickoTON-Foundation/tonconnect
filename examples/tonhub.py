from tonconnect.connector import Connector


connector = Connector('https://tonclick.online/ton-connect.json', use_tonapi=True, tonapi_token=None)
# Currently tonhub working only using tonapi.io
url = connector.connect('tonhub', 'test')

print(f'Universal connect url for Tonhub: {url}')

address = connector.get_address()
print(f'Successfuly connected {address}.')
