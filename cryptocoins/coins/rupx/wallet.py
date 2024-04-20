import logging
from django.db import transaction
from core.models.cryptocoins import UserWallet
from cryptocoins.coins.rupx.utils import create_rupx_address

log = logging.getLogger(__name__)

@transaction.atomic
def get_or_create_rupx_wallet(user_id, is_new=False):
    user_wallet = UserWallet.objects.filter(
        user_id=user_id,
        currency='RUPX',
        blockchain_currency='RUPX',
        is_old=False,
    ).order_by('-id').first()

    if not is_new and user_wallet is not None:
        return user_wallet

    address, encrypted_key = create_rupx_address()
    user_wallet = UserWallet.objects.create(
        user_id=user_id,
        address=address,
        private_key=encrypted_key,
        currency='RUPX',
        blockchain_currency='RUPX'
    )
    return user_wallet

def is_valid_rupx_address(address):
    from cryptocoins.coins.rupx.connection import get_rupx_web3
    w3 = get_rupx_web3()
    return w3.is_address(address)