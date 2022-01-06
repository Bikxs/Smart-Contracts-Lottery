import time

from brownie import Lottery
from brownie import network, config, accounts

from scripts.helpful_scripts import get_account, get_contract, fund_with_link


def deploy_lottery():
    account = get_account()
    aggregator = get_contract("eth_usd_price_feed")
    vrf_coordinator = get_contract("vrf_coordinator")
    link_token = get_contract("link_token")
    fee = config["networks"][network.show_active()]["fee"]
    key_hash = config["networks"][network.show_active()]["key_hash"]
    publish_source = config["networks"][network.show_active()]["verify"]
    lottery = Lottery.deploy(aggregator.address,
                             vrf_coordinator.address,
                             link_token.address,
                             fee,
                             key_hash,
                             {"from": account},
                             publish_source=publish_source)

    print("Deployed Lottery")
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    tx_start_lottery = lottery.startLottery({"from": account})
    tx_start_lottery.wait(1)
    print("The lottery is started")


def enter_lotteries():
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100
    for x in range(10):
        account = accounts[x]
        tx_enter_lottery = lottery.enter({"from": account, "value": value})
        tx_enter_lottery.wait(1)
        print(f"{account} entered the lottery")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # fund the account contract with some LINK
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    tx_end_lottery = lottery.endLottery({"from": account})
    tx_end_lottery.wait(1)
    # end the lottery
    time.sleep(60)
    print(f"Lottery has been ended")
    print(f"{lottery.recentWinner()} if the new winner")



def main():
    deploy_lottery()
    start_lottery()
    enter_lotteries()
    end_lottery()
