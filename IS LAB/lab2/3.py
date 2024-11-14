import time
from Crypto.Cipher import DES, AES #type:ignore
from Crypto.Util.Padding import pad, unpad # type: ignore

def des_encrypt(plaintext, key):
    cipher = DES.new(key, DES.MODE_CBC)
    padded_plaintext = pad(plaintext.encode(), DES.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)
    return cipher.iv + ciphertext  # Prepend IV for decryption

def des_decrypt(ciphertext, key):
    iv = ciphertext[:DES.block_size]
    actual_ciphertext = ciphertext[DES.block_size:]
    cipher = DES.new(key, DES.MODE_CBC, iv)
    decrypted_padded_plaintext = cipher.decrypt(actual_ciphertext)
    return unpad(decrypted_padded_plaintext, DES.block_size).decode()

def aes_encrypt(plaintext, key):
    cipher = AES.new(key.encode(), AES.MODE_CBC)
    padded_plaintext = pad(plaintext.encode(), AES.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)
    return cipher.iv + ciphertext  # Prepend IV for decryption

def aes_decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    actual_ciphertext = ciphertext[AES.block_size:]
    cipher = AES.new(key.encode(), AES.MODE_CBC, iv)
    decrypted_padded_plaintext = cipher.decrypt(actual_ciphertext)
    return unpad(decrypted_padded_plaintext, AES.block_size).decode()

# Example usage
plaintext = "Performance Testing of Encryption Algorithms"
des_key = b'12345678'  # Key must be 8 bytes long for DES
aes_key = "0123456789ABCDEF0123456789ABCDEF"  # 32 bytes long for AES-256

# Measure DES encryption time
start_time = time.time()
des_ciphertext = des_encrypt(plaintext, des_key)
des_encryption_time = time.time() - start_time

# Measure DES decryption time
start_time = time.time()
des_decrypted_message = des_decrypt(des_ciphertext, des_key)
des_decryption_time = time.time() - start_time

# Measure AES encryption time
start_time = time.time()
aes_ciphertext = aes_encrypt(plaintext, aes_key)
aes_encryption_time = time.time() - start_time

# Measure AES decryption time
start_time = time.time()
aes_decrypted_message = aes_decrypt(aes_ciphertext, aes_key)
aes_decryption_time = time.time() - start_time

# Print results
print(f"DES Encryption Time: {des_encryption_time:.6f} seconds")
print(f"DES Decryption Time: {des_decryption_time:.6f} seconds")
print(f"AES Encryption Time: {aes_encryption_time:.6f} seconds")
print(f"AES Decryption Time: {aes_decryption_time:.6f} seconds")

# Verify decrypted messages
print(f"DES Decrypted Message: {des_decrypted_message}")
print(f"AES Decrypted Message: {aes_decrypted_message}")