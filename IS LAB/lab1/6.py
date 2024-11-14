import math  # Importing math module for gcd function

def mod_inverse(a, m):
    """Finds the modular inverse of a under modulo m."""
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def affine_decrypt(ciphertext, a, b):
    """Decrypts an affine cipher given a and b."""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    m = len(alphabet)
    decrypted_text = ""

    # Calculate the modular inverse of a
    a_inv = mod_inverse(a, m)
    
    if a_inv is None:
        return None  # No valid decryption possible with this key

    for char in ciphertext:
        if char in alphabet:
            c = alphabet.index(char)
            # Apply decryption formula
            p = (a_inv * (c - b)) % m
            decrypted_text += alphabet[p]
        else:
            decrypted_text += char  # Non-alphabetic characters remain unchanged

    return decrypted_text

def brute_force_affine(ciphertext):
    """Brute-force attack to find possible keys for an Affine Cipher."""
    alphabet_size = 26
    possible_keys = []

    # Iterate through possible values for a
    for a in range(1, alphabet_size):
        if math.gcd(a, alphabet_size) == 1:  # Ensure a and m are coprime
            # Iterate through possible values for b
            for b in range(0, alphabet_size):
                decrypted_text = affine_decrypt(ciphertext, a, b)
                possible_keys.append((a, b, decrypted_text))

    return possible_keys

# Example usage
ciphertext = "XPALASXYFGFUKPXUSOGEUTKCDGEXANMGNVS"
results = brute_force_affine(ciphertext)

# Print results that likely make sense as English text
for key in results:
    a, b, decrypted_text = key
    print(f"Key (a={a}, b={b}): {decrypted_text}")