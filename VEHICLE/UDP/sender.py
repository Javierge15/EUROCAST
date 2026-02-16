import socket
import json
import time
import csv
import os

TARGET_IP = os.getenv('TARGET_IP', '127.0.0.1')
UDP_PORT = int(os.getenv('UDP_PORT', 5005))
FREQ = 50
FILENAME = f"UDP_RTT_DATA_{int(time.time())}.csv"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.5) 

print(f"UDP SENDER (RTT MODE) -> {TARGET_IP}:{UDP_PORT}")

# Abrimos el archivo y usamos flush para evitar que el CSV quede vacío
with open(FILENAME, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["seq", "rtt_ms", "status", "timestamp"])
    f.flush() # Escribir cabecera inmediatamente

    seq = 0
    try:
        while True:
            cycle_start = time.time()
            t_send = time.time()
            data = {"seq": seq}
            msg = json.dumps(data).encode()
            
            sock.sendto(msg, (TARGET_IP, UDP_PORT))
            
            try:
                echo, _ = sock.recvfrom(4096)
                t_recv = time.time()
                rtt_ms = (t_recv - t_send) * 1000.0
                status = "OK"
            except socket.timeout:
                rtt_ms = -1
                status = "LOST"
                t_recv = time.time()

            # Escribir fila
            writer.writerow([seq, f"{rtt_ms:.3f}", status, f"{t_recv:.6f}"])
            
            # FORZAR ESCRITURA EN DISCO (Esto evita el archivo vacío)
            f.flush()
            os.fsync(f.fileno())

            seq += 1
            elapsed = time.time() - cycle_start
            time.sleep(max(0, (1.0/FREQ) - elapsed))

    except KeyboardInterrupt:
        print("\nFINALIZADO POR USUARIO. ARCHIVO GUARDADO.")
    finally:
        f.close()
        sock.close()