import pytest
from brownie import network, exceptions
from web3 import Web3

from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, fund_with_link, get_contract
from scripts.manage_lottery import deploy_lottery


def test_get_entrance_fee():
    if not network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    entrance_fee = lottery.getEntranceFee()
    expected_entrance_fee = Web3.toWei(0.025, "ether")
    assert entrance_fee == expected_entrance_fee


def test_cannot_enter_unless_started():
    if not network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    value = lottery.getEntranceFee() + 100
    account = get_account()
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": account, "value": value})


def test_can_start_and_enter():
    if not network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    lottery = deploy_lottery()

    # start lottery
    tx_start_lottery = lottery.startLottery({"from": account})
    tx_start_lottery.wait(1)

    value = lottery.getEntranceFee() + 100
    tx_enter_lottery = lottery.enter({"from": account, "value": value})
    tx_enter_lottery.wait(1)

    assert lottery.players(0) == account


def test_can_end():
    if not network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    lottery = deploy_lottery()

    # start lottery
    tx_start_lottery = lottery.startLottery({"from": account})
    tx_start_lottery.wait(1)

    fund_with_link(lottery.address)
    lottery.endLottery({"from": account})

    assert lottery.lottery_state() == 2


def test_can_pick_winner():
    if not network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    lottery = deploy_lottery()

    # start lottery
    tx_start_lottery = lottery.startLottery({"from": account})
    tx_start_lottery.wait(1)
    value = lottery.getEntranceFee() + 100
    lottery.enter({"from": get_account(index=1), "value": value})
    lottery.enter({"from": get_account(index=2), "value": value})
    lottery.enter({"from": get_account(index=3), "value": value})

    starting_balance_of_account = get_account(index=1).balance()
    lottery_balance = lottery.balance()
    fund_with_link(lottery.address)

    tx_end_lottery = lottery.endLottery({"from": account})
    assert lottery.lottery_state() == 2
    requestId = tx_end_lottery.events["RequestRandomness"]["requestId"]
    vrf_coordinator = get_contract("vrf_coordinator")
    STATIC_RNG = 777
    vrf_coordinator.callBackWithRandomness(requestId, STATIC_RNG, lottery.address, {"from": account})
    assert lottery.lottery_state() == 1
    assert lottery.recentWinner() == get_account(index=1)
    assert lottery.balance() == 0
    assert get_account(index=1).balance() == starting_balance_of_account + lottery_balance
