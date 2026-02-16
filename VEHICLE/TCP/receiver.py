import socket
import os

TCP_PORT = int(os.getenv('TCP_PORT', 5005))
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind(("0.0.0.0", TCP_PORT))
server_sock.listen(1)

print(f"TCP MIRROR RECEIVER on port {TCP_PORT}...")

while True:
    conn, addr = server_sock.accept()
    print(f"Client connected: {addr}")
    try:
        while True:
            data = conn.recv(4096)
            if not data: break
            conn.sendall(data)
    except Exception as e:
        print(f"Connection closed: {e}")
    finally:
        conn.close()