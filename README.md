# TON Connect for Python

Library for connecting TON Connect to Python apps.

## Description

At this moment you can connect wallets to apps using HTTP Bridge.

## Getting Started

### Dependencies

* PyNaCl
* tonsdk (will be removed in the future)
* aiohttp
* requests

### Installing

```
git clone https://github.com/ClickoTON-Foundation/tonconnect.git
pip install -e tonconnect
```

### Using

Example of connecting wallet.

```python
from tonconnect.connector import Connector


connector = Connector('https://tonclick.online/ton-connect.json')
url = connector.connect('tonkeeper', 'test')

print(f'Universal connect url for Tonkeeper: {url}')

address = connector.get_address()
print(f'Successfuly connected {address}.')
```

Example of connecting wallet with help of tonapi.io.
tonapi.io it's used to obtain a public key, which adds support for all versions of the wallet that have the get_public_key method. (These are all versions except v3r1).
But if the wallet isn't already deployed, user will not be able to log in.

```python
from tonconnect.connector import Connector


connector = Connector('https://tonclick.online/ton-connect.json', use_tonapi=True, tonapi_token=None)
url = connector.connect('tonkeeper', 'test')

print(f'Universal connect url for Tonkeeper: {url}')

address = connector.get_address()
print(f'Successfuly connected {address}.')
```

Example of asynchronous connecting wallet.

```python
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
```

## Authors

[@Vlad10081](https://t.me/dalvgames)

## Version History

* 0.1.1
    * Added tonapi.io support
* 0.1.0
    * Async wrapper
* 0.0.2 & 0.0.3
    * pyproject.toml fix
* 0.0.1
    * Initial Beta

## License

This project is licensed under the Apache License 2.0 - see the LICENSE.md file for details

## Donate

If you like the library, I will be glad to accept donations.

* TON: EQCgphx8rTI0PukwmgpVqiPgqguTujhQscg2h7jgc4U0t347

## Acknowledgments

* [ton-connect-docs](https://github.com/ton-blockchain/ton-connect)
* [ton-connect-js-sdk](https://github.com/ton-connect/sdk)
