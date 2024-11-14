from math import gcd

def is_coprime(a, b):
    return gcd(a, b) == 1

def multiplicative_encrypt(plain_text, key):
    if not is_coprime(key, 26):
        raise ValueError(f"Key {key} is not coprime to 26.")
    
    encrypted = ""
    for char in plain_text:
        if char.isalpha():
            shifted = (ord(char) - ord('A')) * key % 26
            encrypted += chr(shifted + ord('A'))
    return encrypted

def multiplicative_decrypt(cipher_text, key):
    if not is_coprime(key, 26):
        raise ValueError(f"Key {key} is not coprime to 26.")
    
    decrypted = ""
    # Finding modular inverse of the key
    a_inv = pow(key, -1, 26)
    for char in cipher_text:
        if char.isalpha():
            shifted = (ord(char) - ord('A')) * a_inv % 26
            decrypted += chr(shifted + ord('A'))
    return decrypted

# Example usage
message = "I am learning information security".replace(" ", "").upper()
key = 15

try:
    encrypted_message_mult = multiplicative_encrypt(message, key)
    decrypted_message_mult = multiplicative_decrypt(encrypted_message_mult, key)

    print(f"Multiplicative Cipher:\nEncrypted: {encrypted_message_mult}\nDecrypted: {decrypted_message_mult}")
except ValueError as e:
    print(e)