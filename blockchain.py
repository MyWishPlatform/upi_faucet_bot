from json import load
from web3 import Web3

from cache import store
from calc_gas import est_gas

with open('settings/api.json') as file, open('settings/local.json') as secret, open('settings/provider') as prov:
    data = load(file)
    abi = data['result']
    contract_address = data['address']

    private_key = load(secret)['key']

    provider = prov.read().strip('\n')
    w3 = Web3(Web3.WebsocketProvider(provider))

contract = w3.eth.contract(address=contract_address, abi=abi)
account = w3.eth.account.privateKeyToAccount(private_key)
nonce = w3.eth.getTransactionCount(account.address)


def send_tokens(user_id: int, address: str):
    gas, gasprice = est_gas()

    data = {
        'from': account.address,
        'nonce': nonce,
        'gas': gas,
        'gasPrice': gasprice,
    }

    mint = contract.functions.mint(address, 1000 * 10 ** 18)
    trx = mint.buildTransaction(data)
    signed = account.signTransaction(trx)
    hsh = w3.eth.sendRawTransaction(signed.rawTransaction)

    store(user_id, address)
    return hsh.hex()


def validate_address(address: str):
    return w3.isAddress(address) and w3.isChecksumAddress(address)
