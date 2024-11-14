import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import json

# AES encryption and decryption functions
def generate_key():
    return os.urandom(16)  # Generate a random 128-bit key

def encrypt(key, plaintext):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return cipher.iv + ct_bytes  # Prepend IV for decryption

def decrypt(key, ciphertext):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ciphertext[AES.block_size:]), AES.block_size)
    return pt.decode()

# Step 1a: Create a dataset
documents = {
    1: "The quick brown fox jumps over the lazy dog.",
    2: "Never gonna give you up, never gonna let you down.",
    3: "To be or not to be, that is the question.",
    4: "All that glitters is not gold.",
 
}

# Step 1b: Implement encryption and decryption functions
key = generate_key()
encrypted_documents = {doc_id: encrypt(key, text) for doc_id, text in documents.items()}

# Print encrypted documents
print("Encrypted Documents:")
for doc_id, enc_text in encrypted_documents.items():
    print(f"Doc ID {doc_id}: {enc_text.hex()}")

# Step 1c: Create an inverted index
inverted_index = {}
for doc_id, text in documents.items():
    for word in text.split():
        word = word.lower().strip('.,')  # Normalize word
        if word not in inverted_index:
            inverted_index[word] = []
        inverted_index[word].append(doc_id)

# Encrypt the inverted index
encrypted_index = {word: encrypt(key, json.dumps(doc_ids)) for word, doc_ids in inverted_index.items()}

# Print encrypted inverted index
print("\nEncrypted Inverted Index:")
for word, enc_doc_ids in encrypted_index.items():
    print(f"Word '{word}': {enc_doc_ids.hex()}")

# Step 1d: Implement the search function
def search(query):
    encrypted_query = encrypt(key, query)
    
    # Search for matching terms in the encrypted index
    matching_docs = []
    
    for word in inverted_index.keys():
        if query.lower() == word:
            doc_ids_json = decrypt(key, encrypted_index[word])
            matching_docs.extend(json.loads(doc_ids_json))
    
    # Decrypt document IDs and return corresponding documents
    return [documents[doc_id] for doc_id in set(matching_docs)]

# Example search query
search_query = "the"
results = search(search_query)

# Print results
print(f"\nSearch Results for '{search_query}':")
for result in results:
    print(result)