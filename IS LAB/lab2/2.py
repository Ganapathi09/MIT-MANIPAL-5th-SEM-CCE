from Crypto.Cipher import AES # type: ignore
from Crypto.Util.Padding import pad, unpad # type: ignore
import binascii

def aes_encrypt(plaintext, key):
    # Create a new AES cipher object
    cipher = AES.new(key.encode(), AES.MODE_CBC)
    
    # Pad plaintext to be a multiple of 16 bytes (AES block size)
    padded_plaintext = pad(plaintext.encode(), AES.block_size)
    
    # Encrypt the padded plaintext
    ciphertext = cipher.encrypt(padded_plaintext)
    
    return cipher.iv + ciphertext  # Prepend IV for decryption

def aes_decrypt(ciphertext, key):
    # Extract the IV from the beginning of the ciphertext
    iv = ciphertext[:AES.block_size]
    actual_ciphertext = ciphertext[AES.block_size:]
    
    # Create a new AES cipher object with the extracted IV
    cipher = AES.new(key.encode(), AES.MODE_CBC, iv)
    
    # Decrypt and unpad the plaintext
    decrypted_padded_plaintext = cipher.decrypt(actual_ciphertext)
    decrypted_plaintext = unpad(decrypted_padded_plaintext, AES.block_size)
    
    return decrypted_plaintext.decode()

# Example usage
key = "0123456789ABCDEF"  # Key must be 16 bytes long for AES-128
plaintext = "Sensitive Information"

# Encrypt the message
ciphertext = aes_encrypt(plaintext, key)
print(f"Ciphertext (hex): {binascii.hexlify(ciphertext)}")

# Decrypt the message
decrypted_message = aes_decrypt(ciphertext, key)
print(f"Decrypted Message: {decrypted_message}")