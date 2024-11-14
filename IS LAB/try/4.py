import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.backends import default_backend

# Define users with clearance levels
users = {
    "Dr. Carter": {"role": "Neurosurgeon", "clearance": "high", "aes_key": None},
    "Technician Sara": {"role": "Technician", "clearance": "medium"},
    "Researcher Mark": {"role": "Researcher", "clearance": "low"}
}

# Generate Diffie-Hellman parameters and keys for key exchange
dh_parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())
private_key_carter = dh_parameters.generate_private_key()
public_key_carter = private_key_carter.public_key()

# Sample medical data
medical_data = b"Sensitive neurology patient data"
print("=== Original Medical Data ===")
print(medical_data)

# Generate AES encryption key using DH key exchange (simulated as sharing for simplicity)
def generate_shared_key(private_key, peer_public_key):
    shared_key = private_key.exchange(peer_public_key)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=os.urandom(16),
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(shared_key)

# Simulating DH key generation for peer (authorized doctor)
peer_private_key = dh_parameters.generate_private_key()
peer_public_key = peer_private_key.public_key()

# Generate shared AES key for Dr. Carter
shared_aes_key = generate_shared_key(private_key_carter, peer_public_key)
users["Dr. Carter"]["aes_key"] = shared_aes_key
print("\n=== AES Key (Generated through DH Key Exchange) ===")
print(shared_aes_key)

# Encrypt data with AES
def aes_encrypt(data, key):
    iv = os.urandom(16)  # AES requires a unique initialization vector
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    return iv + encryptor.update(data) + encryptor.finalize()

encrypted_data = aes_encrypt(medical_data, shared_aes_key)
print("\n=== Encrypted Data ===")
print(encrypted_data)

# Generate HMAC for data integrity
def generate_hmac(data, key):
    h = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
    h.update(data)
    return h.finalize()

data_hmac = generate_hmac(encrypted_data, shared_aes_key)
print("\n=== HMAC for Data Integrity ===")
print(data_hmac)

# Access Control & Decryption
def access_data(user, encrypted_data, expected_hmac):
    if user["clearance"] == "high" and user["aes_key"] is not None:
        key = user["aes_key"]
        
        # Verify HMAC
        try:
            h = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
            h.update(encrypted_data)
            h.verify(expected_hmac)
            print(f"\n=== {user['role']} Data Integrity Verified ===")
        except InvalidSignature:
            print("HMAC verification failed: Data may have been tampered with.")
            return

        # Decrypt data
        iv, data = encrypted_data[:16], encrypted_data[16:]
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(data) + decryptor.finalize()
        print(f"{user['role']} Decrypted Data:")
        print(decrypted_data)
    else:
        print(f"Access denied for {user['role']}: Insufficient clearance level or no AES key available.")

# Attempting access by Dr. Carter (Authorized)
print("\n=== Attempting Decryption by Authorized User (Dr. Carter) ===")
access_data(users["Dr. Carter"], encrypted_data, data_hmac)

# Attempt by Technician Sara (Unauthorized)
print("\n=== Attempt by Technician Sara ===")
access_data(users["Technician Sara"], encrypted_data, data_hmac)

# Anonymized data for Researcher Mark
def get_anonymized_data():
    anonymized_data = b"Anonymized patient data for research purposes"
    print("\n=== Anonymized Data for Researcher Mark ===")
    print(anonymized_data)

get_anonymized_data()

# Revocation of Dr. Carter's AES key
print("\n=== Revocation of Dr. Carter's AES Key ===")
users["Dr. Carter"]["aes_key"] = None

# Attempting access by Dr. Carter after revocation
print("\n=== Attempting Decryption by Dr. Carter after Revocation ===")
access_data(users["Dr. Carter"], encrypted_data, data_hmac)
