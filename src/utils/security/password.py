from bcrypt import checkpw, gensalt, hashpw


def encode_password(password: str) -> bytes:
    salt = gensalt()
    password: bytes = password.encode()
    
    return hashpw(password, salt)


def check_password(new_password: str, password: bytes) -> bool:
    new_password: bytes = new_password.encode()
    
    return checkpw(new_password, password)

