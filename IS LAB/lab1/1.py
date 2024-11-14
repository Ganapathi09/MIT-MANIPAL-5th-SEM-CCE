def additive_encrypt(plain_text, key):
    encrypted = ""
    for char in plain_text:
        if char.isalpha():
            shifted = (ord(char) - ord('A') + key) % 26
            encrypted += chr(shifted + ord('A'))
    return encrypted

def additive_decrypt(cipher_text, key):
    decrypted = ""
    for char in cipher_text:
        if char.isalpha():
            shifted = (ord(char) - ord('A') - key) % 26
            decrypted += chr(shifted + ord('A'))
    return decrypted

# Example usage
message = "I am learning information security".replace(" ", "").upper()
key = 20
encrypted_message = additive_encrypt(message, key)
decrypted_message = additive_decrypt(encrypted_message, key)

print(f"Additive Cipher:\nEncrypted: {encrypted_message}\nDecrypted: {decrypted_message}")