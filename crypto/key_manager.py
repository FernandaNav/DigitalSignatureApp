from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_rsa_keypair(bits: int = 2048):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=bits)
    public_key = private_key.public_key()
    return private_key, public_key

def save_private_key(private_key, path: str, password: bytes = None):
    if password:
        encryption = serialization.BestAvailableEncryption(password)
    else:
        encryption = serialization.NoEncryption()
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=encryption
    )
    with open(path, 'wb') as f:
        f.write(pem)

def save_public_key(public_key, path: str):
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(path, 'wb') as f:
        f.write(pem)

def load_private_key(path: str, password: bytes = None):
    with open(path, 'rb') as f:
        data = f.read()
    return serialization.load_pem_private_key(data, password=password)

def load_public_key(path: str):
    with open(path, 'rb') as f:
        data = f.read()
    from cryptography.hazmat.primitives import serialization
    return serialization.load_pem_public_key(data)
