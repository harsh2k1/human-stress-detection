from passlib.context import CryptContext

def generate_hash_uid(uid):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(uid)

def verify_password(uid, hashed_uid):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(uid, hashed_uid)