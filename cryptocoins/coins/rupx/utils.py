import secrets
from django.conf import settings
from eth_account import Account
from lib.cipher import AESCoderDecoder

def create_rupx_address():
    while True:
        private_key = "0x" + secrets.token_hex(32)
        account = Account.from_key(private_key)
        encrypted_key = AESCoderDecoder(settings.CRYPTO_KEY).encrypt(private_key)
        decrypted_key = AESCoderDecoder(settings.CRYPTO_KEY).decrypt(encrypted_key)
        if decrypted_key.startswith('0x') and len(decrypted_key) == 66:
            break
    return account.address, encrypted_key