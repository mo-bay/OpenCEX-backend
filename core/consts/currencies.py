from dataclasses import dataclass
from typing import List, Tuple, Union, Dict, Optional
from collections.abc import Callable
from core.currency import Currency, TokenParams, CoinParams
from cryptocoins.coins.rupx.wallet import is_valid_rupx_address, get_or_create_rupx_wallet

@dataclass
class BlockchainAccount:
    """
    Blockchain Account Info
    """
    address: str
    private_key: str
    public_key: Optional[str] = None
    redeem_script: Optional[str] = None

ALL_CURRENCIES: List[Currency] = []  # all Currency instances

CURRENCIES_LIST: List[Tuple[int, str]] = []

ERC20_CURRENCIES: Dict[Currency, TokenParams] = {}

TRC20_CURRENCIES: Dict[Currency, TokenParams] = {}

BEP20_CURRENCIES: Dict[Currency, TokenParams] = {}

ERC20_MATIC_CURRENCIES: Dict[Currency, TokenParams] = {}

RUPX_TOKEN_CURRENCIES: Dict[Currency, TokenParams] = {}  # Added Rupaya token currencies

ALL_TOKEN_CURRENCIES: List[Currency] = []

# {<Currency>: <validation_fn>} - for coins
# {<Currency>: {<Currency>: <validation_fn>}} - for tokens
CRYPTO_ADDRESS_VALIDATORS: Union[
    Dict[Currency, Callable],
    Dict[Currency, Dict[str, Callable]],
    dict
] = {}

# {<Currency>: <wallet_creation_fn>} - for coins
# {<Currency>: {<Currency>: <wallet_creation_fn>}} - for tokens
CRYPTO_WALLET_CREATORS: Union[
    Dict[Currency, Callable],
    Dict[Currency, Dict[str, Callable]],
    dict
] = {}

CRYPTO_COINS_PARAMS: Dict[Currency, CoinParams] = {}

CRYPTO_WALLET_ACCOUNT_CREATORS: Dict[Currency, BlockchainAccount] = {}

# Rupaya
RUPX_CURRENCY = Currency(217, 'RUPX', 'Rupaya', 8)

ALL_CURRENCIES.append(RUPX_CURRENCY)
CURRENCIES_LIST.append((RUPX_CURRENCY.code, RUPX_CURRENCY.name))

CRYPTO_ADDRESS_VALIDATORS[RUPX_CURRENCY] = is_valid_rupx_address
CRYPTO_WALLET_CREATORS[RUPX_CURRENCY] = get_or_create_rupx_wallet
CRYPTO_COINS_PARAMS[RUPX_CURRENCY] = CoinParams(217, 0)
CRYPTO_WALLET_ACCOUNT_CREATORS[RUPX_CURRENCY] = create_new_rupx_account