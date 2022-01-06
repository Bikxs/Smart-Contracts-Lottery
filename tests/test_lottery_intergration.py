import time

from brownie import Lottery, accounts, config, network
from web3 import Web3
import pytest

from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, fund_with_link
from scripts.manage_lottery import deploy_lottery


def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    lottery = deploy_lottery()

    # start lottery
    tx_start_lottery = lottery.startLottery({"from": account})
    tx_start_lottery.wait(1)
    value = lottery.getEntranceFee() + 100
    lottery.enter({"from": account, "value": value}).wait(1)
    lottery.enter({"from": account, "value": value}).wait(1)
    lottery.enter({"from": account, "value": value}).wait(1)

    starting_balance_of_account = account.balance()
    lottery_balance = lottery.balance()
    fund_with_link(lottery.address)

    tx_end_lottery = lottery.endLottery({"from": account})
    assert lottery.lottery_state() == 2
    time.sleep(60)
    assert lottery.lottery_state() == 1
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert account.balance() == starting_balance_of_account + lottery_balance