from passlib.context import CryptContext

# set up the encryption for password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')


def hash_pass(password: str):
    return pwd_context.hash(password)

def verify_hash(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)