from brownie import Lottery, accounts, config, network
from web3 import Web3


def test_get_entracne_fee():
    account = accounts[0]
    price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    lottery = Lottery.deploy(price_feed_address, {"from": account})
    entraceFee = lottery.getEntranceFee()
    print(f"Entrance Fee: {entraceFee}")
    assert entraceFee > Web3.toWei(0.012, "ether")
    assert entraceFee < Web3.toWei(0.015, "ether")
