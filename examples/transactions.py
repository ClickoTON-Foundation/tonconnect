# WIP, this code isn't working

from tonconnect.connector import AsyncConnector
from tonconnect.requests import SendRequest, SendMessage
import asyncio
import time


async def main():
    connector = AsyncConnector('https://tonclick.online/ton-connect.json', use_tonapi=True)
    url = await connector.connect('tonhub', 'test')

    print(f'Universal connect url for Tonkeeper: {url}')

    address = await connector.get_address()
    print(f'Successfuly connected {address}.')

    request = SendRequest(await connector.wallet.bridge.next_id(), [SendMessage('0:0000000000000000000000000000000000000000000000000000000000000000', 0.000000001), SendMessage('0:0000000000000000000000000000000000000000000000000000000000000000', 0.000000001)], time.time() + 900, -239, '0:a0a61c7cad32343ee9309a0a55aa23e0aa0b93ba3850b1c83687b8e0738534b7')
    print(await connector.bridge.send_request(request))

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
