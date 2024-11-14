import rsa # type: ignore
import hashlib
#pip install rsa
# User definitions
users = {
    "Dr. Smith": {"role": "Doctor", "specialty": "Oncology", "clearance": "high"},
    "Nurse John": {"role": "Nurse", "specialty": "Pediatrics", "clearance": "medium"},
    "Researcher Emily": {"role": "Researcher", "access": "anonymized data"}
}

# Generate RSA keys for Dr. Smith
def generate_keys():
    (public_key, private_key) = rsa.newkeys(2048)
    return public_key, private_key

# Encrypt a message using RSA public key
def encrypt_message(message, public_key):
    return rsa.encrypt(message.encode('utf-8'), public_key)

# Decrypt a message using RSA private key
def decrypt_message(encrypted_message, private_key):
    return rsa.decrypt(encrypted_message, private_key).decode('utf-8')

# Sign a message using RSA private key
def sign_message(message, private_key):
    return rsa.sign(message.encode('utf-8'), private_key, 'SHA-1')

# Verify the signature of a message
def verify_signature(message, signature, public_key):
    try:
        return rsa.verify(message.encode('utf-8'), signature, public_key) == 'SHA-1'
    except:
        return False

# Generate SHA hash of a file content
def generate_hash(file_content):
    return hashlib.sha256(file_content.encode('utf-8')).hexdigest()

# Check file integrity by comparing hashes
def check_integrity(original_hash, new_content):
    new_hash = generate_hash(new_content)
    return original_hash == new_hash

# Example usage
if __name__ == "__main__":
    # Generate keys for Dr. Smith
    public_key, private_key = generate_keys()

    # Patient's sensitive medical record
    patient_record = "Patient: John Doe, Diagnosis: Stage 2 Cancer"
    
    # Generate hash of the patient record
    original_hash = generate_hash(patient_record)

    # Encrypt the patient record
    encrypted_record = encrypt_message(patient_record, public_key)

    # Dr. Smith signs the encrypted record
    signature = sign_message(patient_record, private_key)

    # Simulating data sharing with Nurse John (who cannot decrypt)
    print("Nurse John attempts to access data:")
    
    if users["Nurse John"]["clearance"] == "medium":
        print("Access denied: Insufficient clearance.")
    
    # Simulating access by Dr. Smith
    print("\nDr. Smith accesses the data:")
    
    decrypted_record = decrypt_message(encrypted_record, private_key)
    
    # Verify signature and integrity
    if verify_signature(decrypted_record, signature, public_key):
        print("Signature verified. Data integrity confirmed.")
        
        # Check integrity of the decrypted record
        if check_integrity(original_hash, decrypted_record):
            print("Data integrity check passed.")
            print("Decrypted Patient Record:", decrypted_record)
        else:
            print("Data integrity check failed.")