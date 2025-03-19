from pygost.gost34112012256 import GOST34112012256
import binascii
from Crypto.Random import get_random_bytes

# Используем гост для хэширования данных
def streebog_hash(data):
    hasher = GOST34112012256()
    hasher.update(data)
    return hasher.digest()

# Перевод бинарных данных в hex строку
def bytes_as_hex(b):
    return binascii.hexlify(b).decode()

# Генерация случайных байтов в качестве ключей
def generate_key_pair():
    private_key = get_random_bytes(32)
    public_key = get_random_bytes(32)   
    return private_key, public_key