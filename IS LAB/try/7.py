from cryptography.fernet import Fernet
import json
import hashlib

# Generate a key for encryption/decryption
def generate_key():
    return Fernet.generate_key()

# Encrypt data using a key
def encrypt_data(key, data):
    f = Fernet(key)
    return f.encrypt(data.encode())

# Decrypt data using a key
def decrypt_data(key, encrypted_data):
    f = Fernet(key)
    return f.decrypt(encrypted_data).decode()

# Store the encrypted data in a dictionary with keywords
def store_data(database, key, data, keyword):
    encrypted_data = encrypt_data(key, data)
    if keyword in database:
        database[keyword].append(encrypted_data)
    else:
        database[keyword] = [encrypted_data]

# Search for data by keyword
def search_data(database, key, keyword):
    if keyword in database:
        results = []
        for encrypted_data in database[keyword]:
            decrypted_data = decrypt_data(key, encrypted_data)
            results.append(decrypted_data)
        return results
    else:
        return []

# User Class
class User:
    def __init__(self, name, clearance_level):
        self.name = name
        self.clearance_level = clearance_level
        self.key = generate_key()  # Each user has a unique encryption key
        self.database = {}

    def store_data(self, data, keyword):
        store_data(self.database, self.key, data, keyword)

    def search_data(self, keyword):
        return search_data(self.database, self.key, keyword)

# Main function to demonstrate searchable encryption
def main():
    # Create users
    dr_smith = User("Dr. Smith", "high")
    nurse_john = User("Nurse John", "medium")
    researcher_emily = User("Researcher Emily", "anonymized")

    # Store some data with keywords
    dr_smith.store_data("Patient sensitive medical record information", "patient_record")
    dr_smith.store_data("Doctor's notes on treatment plan", "doctor_notes")
    dr_smith.store_data("Anonymized patient data for research", "anonymized_data")

    # Searching for data by users
    print("Dr. Smith searches for patient records:")
    patient_records = dr_smith.search_data("patient_record")
    for record in patient_records:
        print(f"Dr. Smith found: {record}")

    print("\nNurse John attempts to search for patient records:")
    nurse_john_results = nurse_john.search_data("patient_record")
    if nurse_john_results:
        for record in nurse_john_results:
            print(f"Nurse John found: {record}")
    else:
        print("Nurse John does not have access to this data.")

    print("\nResearcher Emily searches for anonymized data:")
    anonymized_results = researcher_emily.search_data("anonymized_data")
    for record in anonymized_results:
        print(f"Researcher Emily found: {record}")

if __name__ == "__main__":
    main()
