import socket
import os

UDP_PORT = int(os.getenv('UDP_PORT', 5005))
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", UDP_PORT))

print(f"UDP MIRROR RECEIVER on port {UDP_PORT}...")

while True:
    data, addr = sock.recvfrom(4096)
    # Devolver inmediatamente al emisor
    sock.sendto(data, addr)