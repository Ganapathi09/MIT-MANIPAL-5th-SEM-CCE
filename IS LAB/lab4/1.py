import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import HKDF
import hashlib

class KeyManager:
    def __init__(self):
        self.keys = {}

    def generate_key_pair(self):
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        return private_key, public_key

    def store_key(self, subsystem_name, public_key):
        self.keys[subsystem_name] = public_key

    def get_public_key(self, subsystem_name):
        return self.keys.get(subsystem_name)

class SecureCommunication:
    def __init__(self):
        self.key_manager = KeyManager()

    def encrypt_message(self, message, public_key):
        rsa_key = RSA.import_key(public_key)
        cipher = PKCS1_OAEP.new(rsa_key)
        encrypted_message = cipher.encrypt(message.encode('utf-8'))
        return encrypted_message

    def decrypt_message(self, encrypted_message, private_key):
        rsa_key = RSA.import_key(private_key)
        cipher = PKCS1_OAEP.new(rsa_key)
        decrypted_message = cipher.decrypt(encrypted_message).decode('utf-8')
        return decrypted_message

def main():
    # Initialize the communication system
    comm_system = SecureCommunication()

    # Generate keys for subsystems
    finance_private, finance_public = comm_system.key_manager.generate_key_pair()
    hr_private, hr_public = comm_system.key_manager.generate_key_pair()
    scm_private, scm_public = comm_system.key_manager.generate_key_pair()

    # Store public keys
    comm_system.key_manager.store_key("Finance", finance_public)
    comm_system.key_manager.store_key("HR", hr_public)
    comm_system.key_manager.store_key("SCM", scm_public)

    # Example of sending a secure message from Finance to HR
    message = "Financial report for Q1"
    encrypted_msg = comm_system.encrypt_message(message, hr_public)

    # HR decrypts the message using its private key
    decrypted_msg = comm_system.decrypt_message(encrypted_msg, hr_private)
    
    print(f"Decrypted Message: {decrypted_msg}")

if __name__ == "__main__":
    main()