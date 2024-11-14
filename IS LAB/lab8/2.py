from phe import paillier

# Sample dataset: list of documents (each document is a string of words)
documents = [
    "this is the first document",
    "this document is the second document",
    "and this is the third document",
    
]

# Step 1: Generate Paillier key pair
public_key, private_key = paillier.generate_paillier_keypair()

# Step 2b: Encrypt and decrypt functions using Paillier cryptosystem
def encrypt_word(word):
    """Encrypt a word using the Paillier public key."""
    # Simple encryption of the first character of each word
    return public_key.encrypt(ord(word[0]))

def decrypt_word(encrypted_word):
    """Decrypt an encrypted word using the Paillier private key."""
    return chr(private_key.decrypt(encrypted_word))

# Encrypt a document (encrypt each unique word in the document)
def encrypt_document(doc):
    """Encrypt each word of the document."""
    encrypted_doc = {word: encrypt_word(word) for word in set(doc.split())}
    return encrypted_doc

# Decrypt a document (decrypt each word in the encrypted document)
def decrypt_document(encrypted_doc):
    """Decrypt each word of the document."""
    decrypted_doc = {decrypt_word(enc_word) for enc_word in encrypted_doc.values()}
    return decrypted_doc

# Step 2c: Build the inverted index
def build_inverted_index(docs):
    """Create an inverted index mapping words to document IDs."""
    inverted_index = {}
    for doc_id, doc in enumerate(docs):
        for word in set(doc.split()):  # Unique words in each document
            if word not in inverted_index:
                inverted_index[word] = []
            inverted_index[word].append(doc_id)
    return inverted_index

# Encrypt the inverted index using Paillier
def encrypt_inverted_index(inverted_index):
    """Encrypt the keys (words) in the inverted index using Paillier encryption."""
    encrypted_index = {}
    for word, doc_ids in inverted_index.items():
        encrypted_word = encrypt_word(word)
        encrypted_index[encrypted_word] = doc_ids
    return encrypted_index

# Step 2d: Search encrypted index
def search_encrypted_index(query):
    """Search for a word in the encrypted index and return matching document IDs."""
    encrypted_query = encrypt_word(query)
    
    # Search in the encrypted index
    if encrypted_query in encrypted_inverted_index:
        return encrypted_inverted_index[encrypted_query]
    else:
        return []

# Step 2a: Build the inverted index from the dataset
inverted_index = build_inverted_index(documents)
print("Original Inverted Index: ", inverted_index)

# Encrypt the inverted index
encrypted_inverted_index = encrypt_inverted_index(inverted_index)
print("Encrypted Inverted Index (Paillier Encrypted): ", encrypted_inverted_index)

# Perform a search query (example: search for the word "document")
search_query = "document"
matching_doc_ids = search_encrypted_index(search_query)

if matching_doc_ids:
    print(f"Search Query: {search_query}")
    print(f"Documents containing '{search_query}': {matching_doc_ids}")
else:
    print(f"No documents found for query '{search_query}'")
