import hashlib
import json
import random

# Simple Homomorphic Encryption Class
class HomomorphicEncryption:
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def encrypt(self, plaintext):
        """Encrypt the plaintext using a simple method."""
        return (plaintext + self.secret_key) % 256  # Simple addition-based encryption

    def decrypt(self, ciphertext):
        """Decrypt the ciphertext using the secret key."""
        return (ciphertext - self.secret_key) % 256  # Simple decryption

    def add(self, a, b):
        """Homomorphically add two encrypted values."""
        return (a + b) % 256

    def multiply(self, a, b):
        """Homomorphically multiply two encrypted values (not a true FHE)."""
        return (a * b) % 256  # Simple multiplication for demonstration


# User class definition
class User:
    def __init__(self, name, clearance_level):
        self.name = name
        self.clearance_level = clearance_level
        self.secret_key = random.randint(1, 100)  # Random secret key
        self.encryption = HomomorphicEncryption(self.secret_key)

    def sign_data(self, data):
        """Sign data using SHA-256 hash."""
        return hashlib.sha256(data.encode()).hexdigest()

    def verify_signature(self, data, signature):
        """Verify data signature using SHA-256 hash."""
        return self.sign_data(data) == signature


# Data Integrity with SHA-256
def generate_sha256_hash(data):
    """Generate SHA-256 hash of the data."""
    return hashlib.sha256(data.encode()).hexdigest()


def verify_sha256_hash(original_data, hash_value):
    """Verify if the hash matches the original data."""
    return generate_sha256_hash(original_data) == hash_value


# Main function to demonstrate functionality
def main():
    # Create users
    dr_smith = User("Dr. Smith", "high")
    nurse_john = User("Nurse John", "medium")
    researcher_emily = User("Researcher Emily", "anonymized")

    # Patient medical record
    patient_record = 100  # Simulating a numeric sensitive medical record

    # Dr. Smith encrypts the data
    print("Dr. Smith encrypts the patient record.")
    encrypted_data = dr_smith.encryption.encrypt(patient_record)

    # Generate SHA-256 hash of the original data
    original_hash = generate_sha256_hash(str(patient_record))

    # Dr. Smith signs the data
    signature = dr_smith.sign_data(str(patient_record))

    # Nurse John attempts to access patient record
    print("\nNurse John attempts to access patient record.")
    if nurse_john.clearance_level == "medium":
        # Nurse John can access basic data but not the sensitive info
        print("Nurse John cannot decrypt sensitive data.")
    else:
        decrypted_record = dr_smith.encryption.decrypt(encrypted_data)
        print(f"Nurse John accessed: {decrypted_record}")

    # Verify integrity of the record for Nurse John
    if verify_sha256_hash(str(patient_record), original_hash):
        print("Integrity check passed for Nurse John.")
    else:
        print("Integrity check failed for Nurse John.")

    # Researcher Emily accesses anonymized data
    print("\nResearcher Emily searches for anonymized data.")
    anonymized_data = 200  # Numeric representation of anonymized data
    researcher_hash = generate_sha256_hash(str(anonymized_data))
    print(f"Researcher Emily can access: {anonymized_data}")
    print(f"Integrity of anonymized data verified: {verify_sha256_hash(str(anonymized_data), researcher_hash)}")

    # Dr. Smith sharing with a specialist
    print("\nDr. Smith shares diagnosis with a specialist.")
    shared_data = 150  # Diagnosis represented as numeric
    encrypted_shared_data = dr_smith.encryption.encrypt(shared_data)
    shared_signature = dr_smith.sign_data(str(shared_data))

    # Specialist decrypts and verifies
    print("Specialist receives and verifies the data.")
    decrypted_shared_data = dr_smith.encryption.decrypt(encrypted_shared_data)
    if dr_smith.verify_signature(str(decrypted_shared_data), shared_signature):
        print(f"Specialist verified and accessed data: {decrypted_shared_data}")

    # Homomorphic Operations Example
    print("\nDemonstrating Homomorphic Operations:")
    # Example of homomorphic addition
    encrypted_a = dr_smith.encryption.encrypt(20)
    encrypted_b = dr_smith.encryption.encrypt(30)
    encrypted_sum = dr_smith.encryption.add(encrypted_a, encrypted_b)
    decrypted_sum = dr_smith.encryption.decrypt(encrypted_sum)
    print(f"Homomorphic addition result (20 + 30): {decrypted_sum}")

    # Example of homomorphic multiplication (basic demonstration)
    encrypted_x = dr_smith.encryption.encrypt(3)
    encrypted_y = dr_smith.encryption.encrypt(5)
    encrypted_product = dr_smith.encryption.multiply(encrypted_x, encrypted_y)
    decrypted_product = dr_smith.encryption.decrypt(encrypted_product)
    print(f"Homomorphic multiplication result (3 * 5): {decrypted_product}")

    # Revocation scenario (simulated)
    print("\nRevocation scenario: Dr. Smith's clearance is downgraded.")
    dr_smith = None  # Simulating revocation of access
    print("Dr. Smith's access has been revoked.")


if __name__ == "__main__":
    main()
