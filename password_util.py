from hashlib import scrypt
from os import urandom


def hash_password(password: str):
    salt = urandom(16)
    hash = scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)
    return hash, salt


def check_password(password: str, salt: bytes, hash: bytes):
    return scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1) == hash
