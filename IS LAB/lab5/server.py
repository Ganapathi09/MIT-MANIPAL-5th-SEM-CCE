import socket
import hashlib

def compute_hash(data):
    """Compute SHA-256 hash of the given data."""
    return hashlib.sha256(data).hexdigest()

def run_server():
    host = '127.0.0.1'  # Localhost
    port = 65432        # Port to listen on

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Server listening on {host}:{port}")

        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            data = conn.recv(1024)
            if not data:
                return
            
            print(f"Received data: {data.decode()}")
            # Compute hash of received data
            hash_value = compute_hash(data)
            print(f"Computed Hash: {hash_value}")
            
            # Send back the hash value
            conn.sendall(hash_value.encode())

if __name__ == "__main__":
    run_server()