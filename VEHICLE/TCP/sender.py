import socket
import json
import time
import csv
import os

TARGET_IP = os.getenv('TARGET_IP', '127.0.0.1')
TCP_PORT = int(os.getenv('TCP_PORT', 5005)) 
FREQ = 50
FILENAME = f"TCP_RTT_DATA_{int(time.time())}.csv"

print(f"TCP SENDER (RTT MODE) -> {TARGET_IP}:{TCP_PORT}")

while True:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        sock.connect((TARGET_IP, TCP_PORT))
        print("CONNECTED")
        break
    except ConnectionRefusedError:
        print("NOT CONNECTED. RETRYING...")
        time.sleep(2)

with open(FILENAME, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["seq", "rtt_ms", "inter_arrival_ms", "timestamp"])
    f.flush()
    
    seq = 0
    last_recv_ts = 0
    
    try:
        while True:
            cycle_start = time.time()
            t_send = time.time()
            data = {"seq": seq, "t_send": t_send}
            msg = json.dumps(data) + "\n"
            
            sock.sendall(msg.encode())
            
            echo_buffer = b""
            while b"\n" not in echo_buffer:
                chunk = sock.recv(1024)
                if not chunk: break
                echo_buffer += chunk
            
            t_recv = time.time()
            rtt_ms = (t_recv - t_send) * 1000.0
            
            inter_arrival_ms = 0.0
            if last_recv_ts != 0:
                inter_arrival_ms = (t_recv - last_recv_ts) * 1000.0
            
            writer.writerow([seq, f"{rtt_ms:.3f}", f"{inter_arrival_ms:.3f}", f"{t_recv:.6f}"])
            
            f.flush()
            os.fsync(f.fileno())
            
            last_recv_ts = t_recv
            seq += 1
            
            elapsed = time.time() - cycle_start
            time.sleep(max(0, (1.0/FREQ) - elapsed))

    except (KeyboardInterrupt, BrokenPipeError):
        print("\nCONEXIÓN CERRADA. ARCHIVO GUARDADO.")
    finally:
        f.close()
        sock.close()