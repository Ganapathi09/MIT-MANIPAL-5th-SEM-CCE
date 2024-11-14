from cryptography.hazmat.primitives.asymmetric import ec    #type:ignore
from cryptography.hazmat.primitives import serialization#type:ignore
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt#type:ignore
from cryptography.hazmat.primitives import hashes#type:ignore
from cryptography.hazmat.backends import default_backend#type:ignore
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes#type:ignore
import os
#pip install cryptography
# Generate ECC private and public keys
private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
public_key = private_key.public_key()

# Serialize public key for display (optional)
pub_key_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Message to encrypt
message = b"Secure Transactions"

# Derive shared secret from public key
shared_secret = private_key.exchange(ec.ECDH(), public_key)

# Derive a symmetric key from the shared secret
kdf = Scrypt(
    salt=os.urandom(16),
    length=32,
    n=2**14,
    r=8,
    p=1,
)
symmetric_key = kdf.derive(shared_secret)

# Encrypt the message using AES
iv = os.urandom(16)  # Generate a random IV
cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv), backend=default_backend())
encryptor = cipher.encryptor()

# Pad message to be multiple of block size (16 bytes for AES)
pad_length = 16 - len(message) % 16
padded_message = message + bytes([pad_length] * pad_length)

ciphertext = encryptor.update(padded_message) + encryptor.finalize()

print("Ciphertext:", ciphertext)

# Decrypting the message using the same symmetric key
decryptor = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv), backend=default_backend()).decryptor()
decrypted_padded_message = decryptor.update(ciphertext) + decryptor.finalize()

# Remove padding
pad_length = decrypted_padded_message[-1]
decrypted_message = decrypted_padded_message[:-pad_length]

print("Decrypted Message:", decrypted_message.decode())