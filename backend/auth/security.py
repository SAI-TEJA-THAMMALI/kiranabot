from argon2 import PasswordHasher
ph = PasswordHasher()
def hash_password(password:str)->str:
    return ph.hash(password)
def verify_password(password:str,hash_password:str)->bool:
    try:
        ph.verify(hash_password,password)
        return True
    except:
        return False