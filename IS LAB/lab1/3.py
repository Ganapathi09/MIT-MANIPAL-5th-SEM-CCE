def create_playfair_matrix(key):
    key = key.upper().replace("J", "I")  # Treat 'J' as 'I'
    matrix = []
    seen = set()

    # Fill matrix with key characters
    for char in key:
        if char not in seen and char.isalpha():
            seen.add(char)
            matrix.append(char)

    # Fill matrix with remaining characters
    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":  # Note: 'J' is omitted
        if char not in seen:
            seen.add(char)
            matrix.append(char)

    return [matrix[i:i + 5] for i in range(0, 25, 5)]  # Create 5x5 matrix

def prepare_plaintext(plaintext):
    plaintext = plaintext.upper().replace(" ", "").replace("J", "I")
    digraphs = []
    
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

def encrypt_playfair(plaintext, key):
    matrix = create_playfair_matrix(key)
    digraphs = prepare_plaintext(plaintext)
    
    encrypted_text = ""
    
    # Create a mapping of characters to their positions in the matrix
    position_map = {}
    for r in range(5):
        for c in range(5):
            position_map[matrix[r][c]] = (r, c)

    for digraph in digraphs:
        row1, col1 = position_map[digraph[0]]
        row2, col2 = position_map[digraph[1]]

        if row1 == row2:  # Same row
            encrypted_text += matrix[row1][(col1 + 1) % 5]
            encrypted_text += matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:  # Same column
            encrypted_text += matrix[(row1 + 1) % 5][col1]
            encrypted_text += matrix[(row2 + 1) % 5][col2]
        else:  # Rectangle swap
            encrypted_text += matrix[row1][col2]
            encrypted_text += matrix[row2][col1]

    return encrypted_text

# Example usage
message = "The key is hidden under the door pad"
key = "GUIDANCE"

encrypted_message = encrypt_playfair(message, key)
print(f"Encrypted Message: {encrypted_message}")