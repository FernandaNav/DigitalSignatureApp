from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key

def sign_file_with_private_key(priv_path: str, file_path: str) -> str:
    with open(priv_path, 'rb') as f:
        priv = load_pem_private_key(f.read(), password=None)
    with open(file_path, 'rb') as f:
        data = f.read()
    signature = priv.sign(
        data,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
    out = file_path + ".sig"
    with open(out, 'wb') as f:
        f.write(signature)
    return out

def verify_file_with_public_key(pub_path: str, file_path: str, sig_path: str) -> bool:
    with open(pub_path, 'rb') as f:
        pub = load_pem_public_key(f.read())
    with open(file_path, 'rb') as f:
        data = f.read()
    with open(sig_path, 'rb') as f:
        sig = f.read()
    try:
        pub.verify(
            sig,
            data,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False
