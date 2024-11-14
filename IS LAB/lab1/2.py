def generate_key(plain_text, key):
    key = list(key)
    if len(plain_text) == len(key):
        return key
    else:
        for i in range(len(plain_text) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)

def vigenere_encrypt(plain_text, key):
    plain_text = plain_text.replace(" ", "").upper()
    key = generate_key(plain_text, key).upper()
    cipher_text = ""
    
    for i in range(len(plain_text)):
        x = (ord(plain_text[i]) + ord(key[i])) % 26
        cipher_text += chr(x + ord('A'))
    
    return cipher_text

def vigenere_decrypt(cipher_text, key):
    key = generate_key(cipher_text, key).upper()
    plain_text = ""
    
    for i in range(len(cipher_text)):
        x = (ord(cipher_text[i]) - ord(key[i]) + 26) % 26
        plain_text += chr(x + ord('A'))
    
    return plain_text

def autokey_encrypt(plain_text, shift):
    plain_text = plain_text.replace(" ", "").upper()
    cipher_text = ""
    
    for i in range(len(plain_text)):
        x = (ord(plain_text[i]) - ord('A') + shift) % 26
        cipher_text += chr(x + ord('A'))
        # Update shift to be the last encrypted character's position
        shift = x
    
    return cipher_text

def autokey_decrypt(cipher_text, initial_shift):
    decrypted = ""
    shift = initial_shift
    
    for i in range(len(cipher_text)):
        x = (ord(cipher_text[i]) - ord('A') - shift + 26) % 26
        decrypted += chr(x + ord('A'))
        # Update shift to be the last decrypted character's position
        shift = x
    
    return decrypted

# Example usage
message = "the house is being sold tonight"
key_vigenere = "dollars"
key_autokey = 7

# Vigenère Cipher
encrypted_message_vigenere = vigenere_encrypt(message, key_vigenere)
decrypted_message_vigenere = vigenere_decrypt(encrypted_message_vigenere, key_vigenere)

# Autokey Cipher
encrypted_message_autokey = autokey_encrypt(message, key_autokey)
decrypted_message_autokey = autokey_decrypt(encrypted_message_autokey, key_autokey)

# Output results
print(f"Vigenère Cipher:\nEncrypted: {encrypted_message_vigenere}\nDecrypted: {decrypted_message_vigenere}\n")
print(f"Autokey Cipher:\nEncrypted: {encrypted_message_autokey}\nDecrypted: {decrypted_message_autokey}")