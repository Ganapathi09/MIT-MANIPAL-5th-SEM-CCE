from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
import os
#pip install cryptography

# Sample users with access levels
users = {
    "Dr. Miller": {"role": "Cardiologist", "clearance": "high", "key": None},
    "Nurse Grace": {"role": "Nurse in Orthopedics", "clearance": "medium", "key": None},
    "Researcher Alan": {"role": "Researcher", "clearance": "low", "key": None}
}

# Generate asymmetric keys for ElGamal-style encryption (simulated with RSA)
def generate_keypair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    public_key = private_key.public_key()
    return private_key, public_key

# Assign keys to users with high clearance
dr_miller_private_key, dr_miller_public_key = generate_keypair()
users["Dr. Miller"]["key"] = (dr_miller_private_key, dr_miller_public_key)

# Sample medical data
medical_data = b"Sensitive cardiology patient data"
print("=== Original Medical Data ===")
print(medical_data)

# Generate a SHA-256 hash for data integrity
data_hash = hashes.Hash(SHA256(), backend=default_backend())
data_hash.update(medical_data)
original_hash = data_hash.finalize()
print("\n=== SHA-256 Hash for Data Integrity ===")
print(original_hash)

# Encrypting data (Simulated ElGamal with RSA)
def encrypt_data(data, public_key):
    encrypted = public_key.encrypt(
        data,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    return encrypted

encrypted_data = encrypt_data(medical_data, dr_miller_public_key)
print("\n=== Encrypted Data ===")
print(encrypted_data)

# Signing data
def sign_data(data, private_key):
    signer = private_key.sign(
        data,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
    return signer

signature = sign_data(encrypted_data, dr_miller_private_key)
print("\n=== Digital Signature ===")
print(signature)

# Access Control & Decryption
def access_data(user, encrypted_data, signature, original_hash):
    if user["clearance"] == "high":
        private_key, public_key = user["key"]
        
        # Verify signature
        try:
            public_key.verify(
                signature,
                encrypted_data,
                padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256()
            )
            print(f"\n=== {user['role']} Signature Verified Successfully ===")
        except InvalidSignature:
            print(f"\n=== Signature Verification Failed for {user['role']} ===")
            return
        
        # Decrypt data
        try:
            decrypted_data = private_key.decrypt(
                encrypted_data,
                padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
            )
            # Verify data integrity
            data_hash = hashes.Hash(SHA256(), backend=default_backend())
            data_hash.update(decrypted_data)
            if data_hash.finalize() == original_hash:
                print(f"Data integrity verified for {user['role']}. Decrypted Data:")
                print(decrypted_data)
            else:
                print("Data integrity check failed.")
        except Exception as e:
            print("Decryption failed:", str(e))
    else:
        print(f"Access denied for {user['role']}: Insufficient clearance level.")

# Attempting access by Dr. Miller (Authorized)
print("\n=== Attempting Decryption by Authorized User (Dr. Miller) ===")
access_data(users["Dr. Miller"], encrypted_data, signature, original_hash)

# Attempt by Nurse Grace (Unauthorized)
print("\n=== Attempt by Nurse Grace ===")
access_data(users["Nurse Grace"], encrypted_data, signature, original_hash)

# Providing anonymized data for Researcher Alan
def get_anonymized_data():
    anonymized_data = b"Anonymized patient data for research purposes"
    print("\n=== Anonymized Data for Researcher Alan ===")
    print(anonymized_data)

get_anonymized_data()

# Revocation of Dr. Miller's Access (Simulating removal of private key)
print("\n=== Revocation of Dr. Miller's Private Key ===")
users["Dr. Miller"]["key"] = (None, dr_miller_public_key)  # Nullify private key for Dr. Miller

# Attempting access by Dr. Miller after revocation
print("\n=== Attempting Decryption by Dr. Miller after Revocation ===")
access_data(users["Dr. Miller"], encrypted_data, signature, original_hash)
