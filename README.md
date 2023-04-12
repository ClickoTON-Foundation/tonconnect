# TON Connect for Python

Library for connecting TON Connect to Python apps.

## Description

At this moment you can connect wallets to apps using HTTP Bridge.

## Getting Started

### Dependencies

* PyNaCl
* tonsdk (will be removed in the future)

### Installing

```
git clone https://github.com/ClickoTON-Foundation/tonconnect.git
pip install -e tonconnect
```

### Using

Example of connecting wallet.

```
from tonconnect.connector import Connector


connector = Connector('https://tonclick.online/ton-connect.json')
url = connector.connect('tonkeeper', 'test')

print(f'Universal connect url for Tonkeeper: {url}')

address = connector.get_address()
print(f'Successfuly connected {address}.')
```

## Authors

[@Vlad10081](https://t.me/dalvgames)

## Version History

* 0.0.1
    * Initial Beta

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Acknowledgments

* [ton-connect-docs](https://github.com/ton-blockchain/ton-connect)
* [ton-connect-js-sdk](https://github.com/ton-connect/sdk)