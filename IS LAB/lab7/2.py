import random
from sympy import mod_inverse

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def generate_keypair(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Choose e such that 1 < e < phi and gcd(e, phi) = 1
    e = 3
    while gcd(e, phi) != 1:
        e += 2  # Increment by 2 to ensure e is odd

    d = mod_inverse(e, phi)
    return ((e, n), (d, n))  # Public key and private key

def encrypt(public_key, plaintext):
    e, n = public_key
    # Encrypt: c = (plaintext ** e) % n
    ciphertext = pow(plaintext, e, n)
    return ciphertext

def decrypt(private_key, ciphertext):
    d, n = private_key
    # Decrypt: m = (ciphertext ** d) % n
    plaintext = pow(ciphertext, d, n)
    return plaintext

# Example usage
p = 61  # First prime number
q = 53  # Second prime number
public_key, private_key = generate_keypair(p, q)

# Encrypt two integers
num1 = 7
num2 = 3
encrypted_num1 = encrypt(public_key, num1)
encrypted_num2 = encrypt(public_key, num2)

# Print the ciphertexts
print(f"Ciphertext of {num1}: {encrypted_num1}")
print(f"Ciphertext of {num2}: {encrypted_num2}")

# Perform multiplication on the encrypted integers (this is not standard RSA but demonstrates multiplicative homomorphism)
encrypted_product = (encrypted_num1 * encrypted_num2) % public_key[1]  # Modulus n

# Print the result of the multiplication in encrypted form
print(f"Encrypted product: {encrypted_product}")

# Decrypt the result of the multiplication
decrypted_product = decrypt(private_key, encrypted_product)

# Verify that it matches the product of the original integers
original_product = num1 * num2
print(f"Decrypted product: {decrypted_product}")
print(f"Original product: {original_product}")