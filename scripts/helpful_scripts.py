from brownie import VRFCoordinatorMock, MockV3Aggregator, LinkToken
from brownie import accounts, config, network, Contract, interface
from web3 import Web3

FORKED_LOCAL_ENVIROMENTS = ["mainnet-fork"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
DECIMALS = 8
INITIAL_VALUE = 200000000000


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS + FORKED_LOCAL_ENVIROMENTS:
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken
}


def get_contract(contract_name: str):
    """
    This function will grad the contract address from the brownie config if defined,
     ortherwise it will create a mock version and return it
    :param contract_name: the name of the contract
    :return: brownie.network.contract.ProjectContract: The most recently deployed version of this contract
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if not contract_type:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)
    return contract


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    account = get_account()
    if not MockV3Aggregator:
        print(f"\tDeploying MockV3Aggregator...")
        MockV3Aggregator.deploy(decimals, Web3.toWei(initial_value, "ether"), {"from": account})
    if not LinkToken:
        print(f"\tDeploying LinkToken...")
        LinkToken.deploy({"from": account})
    if not VRFCoordinatorMock:
        print(f"\tDeploying VRFCoordinatorMock...")
        link_address = LinkToken[-1].address
        VRFCoordinatorMock.deploy(link_address, {"from": account})


def fund_with_link(contract_address, account=None, link_token=None, amount=0.1 * (10 ** 18)):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    link_token_contract = interface.LinkTokenInterface(link_token.address)
    link_balance = Web3.fromWei(link_token_contract.balanceOf(account), "ether")
    print(f"Balance of Link in account {account} = {link_balance}")
    tx = link_token_contract.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("The contract has been funded")
    return tx
