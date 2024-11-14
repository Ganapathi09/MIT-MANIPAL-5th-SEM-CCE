import os
import hashlib
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# User definitions
class User:
    def __init__(self, name, clearance):
        self.name = name
        self.clearance = clearance
        self.private_key = random.randint(1, 100)  # Simulated private key
        self.public_key = None
        self.shared_key = None
        self.revoked = False

# Generate a public key for Diffie-Hellman
def generate_public_key(private_key, prime, generator):
    return (generator ** private_key) % prime

# Compute shared key
def compute_shared_key(private_key, other_public_key, prime):
    return (other_public_key ** private_key) % prime

# Encrypt data using AES
def encrypt_data(shared_key, data):
    cipher = AES.new(shared_key.to_bytes(16, 'big'), AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    return cipher.iv + ct_bytes  # Prepend IV for decryption

# Decrypt data using AES
def decrypt_data(shared_key, encrypted_data):
    iv = encrypted_data[:AES.block_size]
    cipher = AES.new(shared_key.to_bytes(16, 'big'), AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data[AES.block_size:]), AES.block_size)
    return decrypted_data

# SHA hash generation
def generate_sha256_hash(data):
    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.digest()

# Revocation of access
def revoke_access(user):
    user.revoked = True
    user.shared_key = None
    print(f"{user.name}'s access has been revoked.")

# Main program
if __name__ == "__main__":
    # Create users
    dr_smith = User("Dr. Smith", "high")
    nurse_john = User("Nurse John", "medium")
    researcher_emily = User("Researcher Emily", "low")

    # Diffie-Hellman parameters
    prime = 23  # A small prime number for demonstration
    generator = 5  # A primitive root modulo prime

    # User 1: Dr. Smith generates his public key
    dr_smith.public_key = generate_public_key(dr_smith.private_key, prime, generator)
    print(f"Dr. Smith's Public Key: {dr_smith.public_key}")

    # User 2: Nurse John generates his public key
    nurse_john.public_key = generate_public_key(nurse_john.private_key, prime, generator)
    print(f"Nurse John's Public Key: {nurse_john.public_key}")

    # Compute shared keys
    dr_smith.shared_key = compute_shared_key(dr_smith.private_key, nurse_john.public_key, prime)
    nurse_john.shared_key = compute_shared_key(nurse_john.private_key, dr_smith.public_key, prime)

    # Patient's sensitive medical record
    medical_record = b"Sensitive medical record information of the patient."

    # Generate SHA hash of the medical record
    original_hash = generate_sha256_hash(medical_record)

    # Encrypt medical record using the shared key
    encrypted_record = encrypt_data(dr_smith.shared_key, medical_record)
    print("\n=== Encrypted Medical Record ===")
    print(encrypted_record)

    # Dr. Smith attempts to access and decrypt the record
    if not dr_smith.revoked:
        decrypted_record = decrypt_data(dr_smith.shared_key, encrypted_record)
        # Verify integrity using SHA hash
        new_hash = generate_sha256_hash(decrypted_record)

        if new_hash == original_hash:
            print("\n=== Decrypted Medical Record ===")
            print(decrypted_record)
            print("Data integrity verified. The record is authentic.")
        else:
            print("Data integrity check failed: Record has been tampered with.")
    else:
        print("Dr. Smith's access is revoked; cannot decrypt records.")

    # Nurse John attempts to access the record
    print("\n=== Nurse John Attempting to Access ===")
    if nurse_john.clearance == "medium":
        print("Access denied: Nurse John can only access basic patient details.")

    # Researcher Emily attempts to access anonymized data
    print("\n=== Researcher Emily Attempting to Access Anonymized Data ===")
    # Simulating access to anonymized data
    anonymized_data = b"Anonymized patient data for research purposes."
    print(anonymized_data)

    # Revocation of Dr. Smith's access
    revoke_access(dr_smith)

    # Dr. Smith attempts to encrypt after revocation
    if not dr_smith.revoked:
        encrypted_record_after_revocation = encrypt_data(dr_smith.shared_key, medical_record)
        print("\n=== Encrypted Medical Record after Revocation ===")
        print(encrypted_record_after_revocation)
    else:
        print("\n=== Dr. Smith's access is revoked; cannot encrypt records. ===")
