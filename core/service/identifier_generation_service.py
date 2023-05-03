import hashlib


def generate_hash_uid(uid):
    identifier = hashlib.sha256(uid.encode()).hexdigest()
    return identifier
