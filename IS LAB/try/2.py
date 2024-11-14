from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature
import hashlib


# Define user roles with clearance levels
class User:
    def __init__(self, name, role, clearance_level):
        self.name = name
        self.role = role
        self.clearance_level = clearance_level
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.public_key = self.private_key.public_key()


# Create instances for users
dr_smith = User("Dr. Smith", "Oncology Doctor", "high")
nurse_john = User("Nurse John", "Pediatrics Nurse", "medium")
researcher_emily = User("Researcher Emily", "Researcher", "low")

# Function to encrypt data using RSA encryption
def rsa_encrypt(data, public_key):
    encrypted_data = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_data

# Function to decrypt data using RSA decryption
def rsa_decrypt(encrypted_data, private_key):
    try:
        decrypted_data = private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_data
    except Exception as e:
        print("Decryption failed:", e)
        return None

# Generate SHA-256 hash of the data
def generate_hash(data):
    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.digest()

# Function to digitally sign data with RSA
def sign_data(data, private_key):
    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

# Function to verify RSA digital signature
def verify_signature(data, signature, public_key):
    try:
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False

# Access control check
def can_access_data(user, required_clearance):
    clearance_levels = {"low": 1, "medium": 2, "high": 3}
    return clearance_levels[user.clearance_level] >= clearance_levels[required_clearance]

# Simulate Dr. Smith accessing and sharing a medical file
medical_data = b"Patient sensitive medical record information"
print("=== Original Medical Data ===")
print(medical_data)

# Step 1: Hash the data for integrity check
original_hash = generate_hash(medical_data)

# Step 2: Encrypt the file (only Dr. Smith has high clearance)
encrypted_data = rsa_encrypt(medical_data, dr_smith.public_key)
print("\n=== Encrypted Data ===")
print(encrypted_data)

# Step 3: Dr. Smith signs the encrypted data
signature = sign_data(encrypted_data, dr_smith.private_key)
print("\n=== Digital Signature ===")
print(signature)

# Attempt to access the data
print("\n=== Attempting Decryption by Authorized User (Dr. Smith) ===")
if verify_signature(encrypted_data, signature, dr_smith.public_key):
    if can_access_data(dr_smith, "high"):  # Dr. Smith requires high clearance
        decrypted_data = rsa_decrypt(encrypted_data, dr_smith.private_key)
        if decrypted_data and generate_hash(decrypted_data) == original_hash:
            print("Data integrity verified. File decrypted successfully:")
            print(decrypted_data)
        else:
            print("Integrity check failed or tampering detected.")
    else:
        print("Access denied: Insufficient clearance level.")

# Simulate Nurse John trying to access the encrypted data with medium clearance (fails)
print("\n=== Attempt by Nurse John ===")
if verify_signature(encrypted_data, signature, dr_smith.public_key):  # Pass Dr. Smith's public_key here
    if can_access_data(nurse_john, "high"):  # Nurse John does not have high clearance
        decrypted_data = rsa_decrypt(encrypted_data, nurse_john.private_key)
        if decrypted_data:
            print("Access granted:", decrypted_data)
        else:
            print("Access denied due to insufficient clearance level.")
    else:
        print("Access denied: Insufficient clearance level for sensitive data.")
else:
    print("Signature verification failed. Unauthorized data modification detected.")

# Simulate Researcher Emily accessing anonymized data
anonymized_data = b"Anonymized patient data for research"
print("\n=== Anonymized Data for Researcher Emily ===")
print(anonymized_data)

# Step 4: Revocation (Dr. Smith's clearance level revoked)
dr_smith.private_key = None  # Simulating private key revocation
print("\n=== Revocation of Dr. Smith's Private Key ===")
decrypted_data = rsa_decrypt(encrypted_data, dr_smith.private_key)
if decrypted_data:
    print("Decryption successful post-revocation:", decrypted_data)
else:
    print("Dr. Smith's access revoked. Decryption failed.")
