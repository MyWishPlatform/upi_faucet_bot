from statistics import median
from web3 import Web3


def est_gas():
    with  open('settings/provider') as prov:
        provider = prov.read().strip('\n')
        w3 = Web3(Web3.WebsocketProvider(provider))

    last_block = w3.eth.get_block(block_identifier='latest')
    trxs = [w3.eth.get_transaction(hsh) for hsh in last_block['transactions']]
    gases = [trx['gas'] for trx in trxs]
    gas_prices = [trx['gasPrice'] for trx in trxs]

    gas = median(gases)
    gas = round(gas)
    gasprice = median(gas_prices)
    gasprice = round(gasprice)
    return gas, gasprice
