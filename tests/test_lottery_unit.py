import pytest
from brownie import network
from web3 import Web3

from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.manage_lottery import deploy_lottery


def test_get_entrance_fee():
    if not network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    entrance_fee = lottery.getEntranceFee()
    expected_entrance_fee = Web3.toWei(0.025, "ether")
    assert entrance_fee == expected_entrance_fee
