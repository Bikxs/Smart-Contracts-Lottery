# Ganache Local
## adding ganache local network
brownie networks add Ethereum ganache-local host=http://127.0.0.1:8545 chainid=1337
## deleting ganache local network
brownie networks delete ganache-local

# Mainnet forking

brownie networks delete mainnet-fork
## infura
brownie networks add development mainnet-fork cmd=ganache-cli host=http://127.0.0.1:8545 fork='https://mainnet.infura.io/v3/$WEB3_INFURA_PROJECT_ID' accounts=10 mnemonic=browmnie port=8545
## alchemy
brownie networks add development mainnet-fork cmd=ganache-cli host=http://127.0.0.1:8545 fork='https://eth-mainnet.alchemyapi.io/v2/$WEB3_ALCHEMY_PROJECT_CODE'  accounts=10 mnemonic=browmnie port=8545


