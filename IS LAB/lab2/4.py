from Crypto.Cipher import DES3 # type: ignore
from Crypto.Util.Padding import pad, unpad # type: ignore
import binascii

def triple_des_encrypt(plaintext, key):
    # Create a Triple DES cipher object
    cipher = DES3.new(key, DES3.MODE_CBC)
    
    # Pad plaintext to be a multiple of 8 bytes (DES block size)
    padded_plaintext = pad(plaintext.encode(), DES3.block_size)
    
    # Encrypt the padded plaintext
    ciphertext = cipher.encrypt(padded_plaintext)
    
    return cipher.iv + ciphertext  # Prepend IV for decryption

def triple_des_decrypt(ciphertext, key):
    # Extract the IV from the beginning of the ciphertext
    iv = ciphertext[:DES3.block_size]
    actual_ciphertext = ciphertext[DES3.block_size:]
    
    # Create a Triple DES cipher object with the extracted IV
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    
    # Decrypt and unpad the plaintext
    decrypted_padded_plaintext = cipher.decrypt(actual_ciphertext)
    decrypted_plaintext = unpad(decrypted_padded_plaintext, DES3.block_size)
    
    return decrypted_plaintext.decode()

# Example usage
key = b'1234567890ABCDEF12345678'  # Key must be 24 bytes long for Triple DES (3DES)
plaintext = "Classified Text"

# Encrypt the message
ciphertext = triple_des_encrypt(plaintext, key)
print(f"Ciphertext (hex): {binascii.hexlify(ciphertext)}")

# Decrypt the message
decrypted_message = triple_des_decrypt(ciphertext, key)
print(f"Decrypted Message: {decrypted_message}")