import os, struct
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key

# Formato del archivo .enc:
# 6 bytes header b"RDENC1"
# 4 bytes (big-endian) length K (RSA-encrypted AES key)
# K bytes: RSA-encrypted AES key
# 12 bytes nonce
# remaining: AES-GCM ciphertext (tag incluido)

HEADER = b"RDENC1"

def load_public_key_from_file(path: str):
    with open(path, 'rb') as f:
        return load_pem_public_key(f.read())

def load_private_key_from_file(path: str):
    with open(path, 'rb') as f:
        return load_pem_private_key(f.read(), password=None)

def hybrid_encrypt_file(pubkey_path: str, infile_path: str) -> str:
    try:
        # load public key
        if not os.path.exists(pubkey_path):
            raise ValueError("No se encontró la clave pública. Genera o selecciona una clave primero.")
        pub = load_public_key_from_file(pubkey_path)
        
        # check input file
        if not os.path.exists(infile_path):
            raise ValueError("No se encontró el archivo a cifrar.")
            
        # generate AES key
        aes_key = AESGCM.generate_key(bit_length=256)
        aesgcm = AESGCM(aes_key)
        nonce = os.urandom(12)
        with open(infile_path, 'rb') as f:
            plaintext = f.read()
        ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    except (ValueError, OSError) as e:
        raise ValueError(f"Error al cifrar el archivo: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error inesperado al cifrar: {str(e)}")
    # encrypt AES key with RSA-OAEP
    enc_key = pub.encrypt(
        aes_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    klen = len(enc_key)
    out_path = infile_path + ".enc"
    with open(out_path, 'wb') as f:
        f.write(HEADER)
        f.write(struct.pack(">I", klen))
        f.write(enc_key)
        f.write(nonce)
        f.write(ciphertext)
    return out_path

def hybrid_decrypt_file(privkey_path: str, enc_path: str) -> str:
    try:
        if not os.path.exists(privkey_path):
            raise ValueError("No se encontró la clave privada. Selecciona una clave primero.")
        if not os.path.exists(enc_path):
            raise ValueError("No se encontró el archivo cifrado.")
            
        priv = load_private_key_from_file(privkey_path)
        with open(enc_path, 'rb') as f:
            header = f.read(len(HEADER))
            if header != HEADER:
                raise ValueError("El archivo no parece estar cifrado (formato no reconocido).")
            klen_bytes = f.read(4)
            klen = struct.unpack(">I", klen_bytes)[0]
            enc_key = f.read(klen)
            nonce = f.read(12)
            ciphertext = f.read()
    except (ValueError, OSError) as e:
        raise ValueError(f"Error al descifrar el archivo: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error inesperado al descifrar: {str(e)}")
    # decrypt AES key
    aes_key = priv.decrypt(
        enc_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    aesgcm = AESGCM(aes_key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    out_path = enc_path + ".dec.txt"
    with open(out_path, 'wb') as f:
        f.write(plaintext)
    return out_path
