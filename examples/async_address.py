import asyncio
from tonconnect.connector import AsyncConnector


async def main():
    connector = AsyncConnector('https://tonclick.online/ton-connect.json')
    url = await connector.connect('tonkeeper', 'test')

    print(f'Universal connect url for Tonkeeper: {url}')

    address = await connector.get_address()
    print(f'Successfuly connected {address}.')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
