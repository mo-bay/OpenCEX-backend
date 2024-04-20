import logging
from web3 import Web3
from web3.middleware import geth_poa_middleware

log = logging.getLogger(__name__)

RUPX_RPC_URL = 'https://rpc.testnet.rupaya.io'

def get_rupx_web3():
    w3 = Web3(Web3.HTTPProvider(RUPX_RPC_URL))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return w3