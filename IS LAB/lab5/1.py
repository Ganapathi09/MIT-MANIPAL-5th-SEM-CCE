def custom_hash(input_string):
    # Initialize the hash value
    hash_value = 5381
    
    # Iterate over each character in the input string
    for char in input_string:
        # Update the hash value using the specified algorithm
        hash_value = ((hash_value << 5) + hash_value) + ord(char)  # Equivalent to hash_value * 33 + ord(char)
        
        # Ensure the hash value is within a 32-bit range
        hash_value &= 0xFFFFFFFF  # Apply a mask to keep it within 32 bits

    return hash_value

# Example usage
if __name__ == "__main__":
    test_string = "Hello, World!"
    hashed_value = custom_hash(test_string)
    print(f"The hash value for '{test_string}' is: {hashed_value}")