from random import randint
from sympy import mod_inverse  # type: ignore

# Function to convert a string to its numeric representation
def string_to_numeric(message):
    return [ord(char) for char in message]

# Function to convert numeric representation back to a string
def numeric_to_string(numbers):
    return ''.join([chr(num) for num in numbers])

# ElGamal encryption function
def elgamal_encrypt(message, p, g, h):
    numeric_message = string_to_numeric(message)
    encrypted_message = []

    # Choose random k
    k = randint(1, p-1)

    # Encryption (c1, c2)
    c1 = pow(g, k, p)
    for M in numeric_message:
        c2 = (M * pow(h, k, p)) % p
        encrypted_message.append((c1, c2))

    return encrypted_message

# ElGamal decryption function
def elgamal_decrypt(ciphertext, p, x):
    decrypted_message = []
    for c1, c2 in ciphertext:
        # Compute the shared secret s = c1^x mod p
        s = pow(c1, x, p)

        # Compute the modular inverse of s
        s_inv = mod_inverse(s, p)

        # Decrypt the message M = (c2 * s^-1) % p
        M = (c2 * s_inv) % p
        decrypted_message.append(M)

    return numeric_to_string(decrypted_message)

# Test the ElGamal encryption and decryption
p = 467  # Example prime number
g = 2    # Example generator
x = 153  # Private key
h = pow(g, x, p)  # h = g^x mod p (part of the public key)

message = "Confidential Data"

# Encrypt the message
ciphertext = elgamal_encrypt(message, p, g, h)
print("Ciphertext:", ciphertext)

# Decrypt the message
decrypted_message = elgamal_decrypt(ciphertext, p, x)
print("Decrypted Message:", decrypted_message)
