from Crypto.Cipher import DES # type: ignore
from Crypto.Util.Padding import pad, unpad # type: ignore
import binascii
#pip install pycryptodome

def des_encrypt(plaintext, key):
    # Create a DES cipher object
    cipher = DES.new(key, DES.MODE_CBC)
    
    # Pad plaintext to be a multiple of 8 bytes (DES block size)
    padded_plaintext = pad(plaintext.encode(), DES.block_size)
    
    # Encrypt the padded plaintext
    ciphertext = cipher.encrypt(padded_plaintext)
    
    return cipher.iv + ciphertext  # Prepend IV for decryption

def des_decrypt(ciphertext, key):
    # Extract the IV from the beginning of the ciphertext
    iv = ciphertext[:DES.block_size]
    actual_ciphertext = ciphertext[DES.block_size:]
    
    # Create a DES cipher object with the extracted IV
    cipher = DES.new(key, DES.MODE_CBC, iv)
    
    # Decrypt and unpad the plaintext
    decrypted_padded_plaintext = cipher.decrypt(actual_ciphertext)
    decrypted_plaintext = unpad(decrypted_padded_plaintext, DES.block_size)
    
    return decrypted_plaintext.decode()

# Example usage
key = b'A1B2C3D4'  # Key must be bytes and 8 bytes long for DES
plaintext = "Confidential Data"

# Encrypt the message
ciphertext = des_encrypt(plaintext, key)
print(f"Ciphertext (hex): {binascii.hexlify(ciphertext)}")

# Decrypt the message
decrypted_message = des_decrypt(ciphertext, key)
print(f"Decrypted Message: {decrypted_message}")