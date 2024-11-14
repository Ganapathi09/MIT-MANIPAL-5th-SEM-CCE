import socket
import hashlib

def compute_hash(data):
    """Compute SHA-256 hash of the given data."""
    return hashlib.sha256(data).hexdigest()

def run_client():
    host = '127.0.0.1'  # The server's hostname or IP address
    port = 65432        # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        
        # Sample data to send
        message = "Hello, Server! This is a test message."
        print(f"Sending data: {message}")
        
        # Compute hash of the message before sending
        local_hash = compute_hash(message.encode())
        print(f"Local Hash: {local_hash}")
        
        client_socket.sendall(message.encode())
        
        # Receive the hash from the server
        received_hash = client_socket.recv(64).decode()
        print(f"Received Hash from Server: {received_hash}")

        # Verify integrity by comparing hashes
        if local_hash == received_hash:
            print("Data integrity verified: Hashes match!")
        else:
            print("Data integrity compromised: Hashes do not match!")

if __name__ == "__main__":
    run_client()