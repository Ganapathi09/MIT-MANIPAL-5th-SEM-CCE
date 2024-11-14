import numpy as np  # type: ignore # Importing NumPy for matrix operations

def create_key_matrix(key):
    return np.array(key).reshape(2, 2)

def prepare_plaintext(plaintext):
    plaintext = plaintext.replace(" ", "").upper()
    digraphs = []

    # Create digraphs
    i = 0
    while i < len(plaintext):
        if i + 1 < len(plaintext):
            if plaintext[i] == plaintext[i + 1]:
                digraphs.append(plaintext[i] + 'X')  # Insert filler 'X'
                i += 1
            else:
                digraphs.append(plaintext[i] + plaintext[i + 1])
                i += 2
        else:
            digraphs.append(plaintext[i] + 'X')  # Last single letter
            i += 1
            
    return digraphs

def encrypt_hill(plaintext, key):
    key_matrix = create_key_matrix(key)
    digraphs = prepare_plaintext(plaintext)
    
    encrypted_text = ""
    
    for digraph in digraphs:
        # Convert letters to numbers (A=0, B=1, ..., Z=25)
        vector = np.array([ord(digraph[0]) - ord('A'), ord(digraph[1]) - ord('A')])
        
        # Matrix multiplication and modulo operation
        encrypted_vector = np.dot(key_matrix, vector) % 26
        
        # Convert back to letters
        encrypted_text += chr(encrypted_vector[0] + ord('A'))
        encrypted_text += chr(encrypted_vector[1] + ord('A'))

    return encrypted_text

# Example usage
message = "We live in an secure india "
key = [3, 3, 2, 7]

encrypted_message = encrypt_hill(message, key)
print(f"Encrypted Message: {encrypted_message}")