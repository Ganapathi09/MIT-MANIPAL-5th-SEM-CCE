def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def modular_inverse(a, m):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

def affine_encrypt(plain_text, a, b):
    encrypted = ""
    for char in plain_text:
        if char.isalpha():
            # Apply the affine transformation
            shifted = (a * (ord(char) - ord('A')) + b) % 26
            encrypted += chr(shifted + ord('A'))
    return encrypted

def affine_decrypt(cipher_text, a, b):
    decrypted = ""
    # Finding modular inverse of 'a'
    a_inv = modular_inverse(a, 26)
    if a_inv is None:
        raise ValueError("The key 'a' must be coprime with 26.")
    
    for char in cipher_text:
        if char.isalpha():
            # Apply the reverse affine transformation
            shifted = (a_inv * ((ord(char) - ord('A')) - b)) % 26
            decrypted += chr(shifted + ord('A'))
    return decrypted

# Example usage
message = "I am learning information security".replace(" ", "").upper()
a_key = 15
b_key = 20

# Encrypting the message
encrypted_message_affine = affine_encrypt(message, a_key, b_key)
# Decrypting the message
decrypted_message_affine = affine_decrypt(encrypted_message_affine, a_key, b_key)

print(f"Affine Cipher:\nEncrypted: {encrypted_message_affine}\nDecrypted: {decrypted_message_affine}")