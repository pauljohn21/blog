import hashlib
import binascii
import random,time

SALT_HASH = "ac00190be2b5ff025c5225febbcaa53b70abf57e659dc7f4da628bf323d0270a"
def generate_password_hash(password,hash_type:str="sha256",salt_length:int=8) -> str:
    if isinstance(password,str):
        byte_password = password.encode()
    else:
        byte_password = password

    salt = "".join(random.sample(SALT_HASH,salt_length))
    byte_salt = salt.encode()

    iterations = 10086

    dk = hashlib.pbkdf2_hmac(hash_name=hash_type,password=byte_password,salt=byte_salt,iterations=iterations)
    str_hash = binascii.hexlify(dk).decode()
    result = "{}:{}:{}".format(hash_type,salt,str_hash)
    return result


def verify_password(password:str,password_hash:str) -> bool:
    hash_password = password_hash.split(":")
    if len(hash_password) != 3:
        return False
    hash_name,salt,password_hash_p = hash_password[0],hash_password[1].encode(),hash_password[2]
    iterations = 10086
    byte_password = password.encode()
    dk = hashlib.pbkdf2_hmac(hash_name=hash_name,password=byte_password,salt=salt,iterations=iterations)
    str_hash = binascii.hexlify(dk).decode()
    if str_hash == password_hash_p:
        return True
    else:
        return False

