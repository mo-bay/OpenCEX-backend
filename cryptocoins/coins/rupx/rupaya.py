import json
import logging
from decimal import Decimal
from typing import Dict, Type

import cachetools.func
from django.conf import settings

from core.consts.currencies import RUPX_TOKEN_CURRENCIES
from core.currency import Currency, TokenParams
from cryptocoins.coins.rupx.connection import get_rupx_web3
from cryptocoins.evm.manager import EVMManager, register_evm_handler
from cryptocoins.interfaces.common import GasPriceCache
from cryptocoins.interfaces.common import Token
from cryptocoins.interfaces.web3_commons import Web3Transaction, Web3CommonHandler

log = logging.getLogger(__name__)

ERC20_ABI = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_from","type":"address"},{"indexed":true,"name":"_to","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_owner","type":"address"},{"indexed":true,"name":"_spender","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Approval","type":"event"}]')  # noqa: 501

RUPX_CURRENCY = Currency(217, 'RUPX', 'Rupaya', 8)
RUPX_CHAIN_ID = 499
RUPX_SAFE_ADDR = '0x1234567890123456789012345678901234567890'  # Replace with the actual safe address

DEFAULT_TRANSFER_GAS_LIMIT = 100_000
DEFAULT_TRANSFER_GAS_MULTIPLIER = 2


class RupxTransaction(Web3Transaction):
    """Rupx tx parser"""


class RupxGasPriceCache(GasPriceCache):
    GAS_PRICE_UPDATE_PERIOD = settings.RUPX_GAS_PRICE_UPDATE_PERIOD
    GAS_PRICE_COEFFICIENT = settings.RUPX_GAS_PRICE_COEFFICIENT
    MIN_GAS_PRICE = settings.RUPX_MIN_GAS_PRICE
    MAX_GAS_PRICE = settings.RUPX_MAX_GAS_PRICE

    @cachetools.func.ttl_cache(ttl=GAS_PRICE_UPDATE_PERIOD)
    def get_price(self):
        return self.web3.eth.gas_price


class RupxToken(Token):
    ABI = ERC20_ABI
    BLOCKCHAIN_CURRENCY: Currency = RUPX_CURRENCY
    CHAIN_ID = RUPX_CHAIN_ID


class RupxManager(EVMManager):
    CURRENCY: Currency = RUPX_CURRENCY
    GAS_CURRENCY = settings.RUPX_TX_GAS
    TOKEN_CURRENCIES: Dict[Currency, TokenParams] = RUPX_TOKEN_CURRENCIES
    TOKEN_CLASS: Type[Token] = RupxToken
    GAS_PRICE_CACHE_CLASS: Type[GasPriceCache] = RupxGasPriceCache
    CHAIN_ID = RUPX_CHAIN_ID
    MIN_BALANCE_TO_ACCUMULATE_DUST = Decimal('0.001')
    COLD_WALLET_ADDRESS = settings.RUPX_SAFE_ADDR


rupx_manager = RupxManager(client=get_rupx_web3())


@register_evm_handler
class RupxHandler(Web3CommonHandler):
    CURRENCY = RUPX_CURRENCY
    COIN_MANAGER = rupx_manager
    TOKEN_CURRENCIES = rupx_manager.registered_token_currencies
    TOKEN_CONTRACT_ADDRESSES = rupx_manager.registered_token_addresses
    TRANSACTION_CLASS = RupxTransaction
    DEFAULT_BLOCK_ID_DELTA = 1000
    SAFE_ADDR = RUPX_SAFE_ADDR
    CHAIN_ID = RUPX_CHAIN_ID
    BLOCK_GENERATION_TIME = 7
    ACCUMULATION_PERIOD = 60
    IS_ENABLED = True
    W3_CLIENT = get_rupx_web3()