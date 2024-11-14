import hashlib
import time
import random
import string

def generate_random_string(length=10):
    """Generate a random string of fixed length."""
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def compute_hashes(data):
    """Compute MD5, SHA-1, and SHA-256 hashes for the given data."""
    hashes = {
        'MD5': [],
        'SHA-1': [],
        'SHA-256': []
    }
    
    for item in data:
        # MD5
        start_time = time.time()
        md5_hash = hashlib.md5(item.encode()).hexdigest()
        hashes['MD5'].append((md5_hash, time.time() - start_time))
        
        # SHA-1
        start_time = time.time()
        sha1_hash = hashlib.sha1(item.encode()).hexdigest()
        hashes['SHA-1'].append((sha1_hash, time.time() - start_time))
        
        # SHA-256
        start_time = time.time()
        sha256_hash = hashlib.sha256(item.encode()).hexdigest()
        hashes['SHA-256'].append((sha256_hash, time.time() - start_time))
    
    return hashes

def detect_collisions(hashes):
    """Detect collisions in the given hash lists."""
    collisions = {
        'MD5': set(),
        'SHA-1': set(),
        'SHA-256': set()
    }
    
    for algo in hashes:
        seen = {}
        for hash_value, _ in hashes[algo]:
            if hash_value in seen:
                collisions[algo].add(hash_value)
            else:
                seen[hash_value] = True
    
    return collisions

def main():
    # Generate a dataset of random strings
    num_strings = 100  # Number of strings to generate
    random_strings = [generate_random_string(random.randint(10, 20)) for _ in range(num_strings)]
    
    # Compute hashes and measure performance
    hashes = compute_hashes(random_strings)
    
    # Detect collisions
    collisions = detect_collisions(hashes)
    
    # Print results
    for algo in hashes:
        print(f"\n{algo} Hashes:")
        total_time = sum(time_taken for _, time_taken in hashes[algo])
        print(f"Total computation time: {total_time:.6f} seconds")
        
        # Print individual hash times
        for hash_value, time_taken in hashes[algo]:
            print(f"Hash: {hash_value}, Time taken: {time_taken:.6f} seconds")
    
    # Print collision results
    print("\nCollisions detected:")
    for algo in collisions:
        if collisions[algo]:
            print(f"{algo}: {len(collisions[algo])} collision(s) detected.")
        else:
            print(f"{algo}: No collisions detected.")

if __name__ == "__main__":
    main()