import cv2
import subprocess
import time
import csv
import os

DEV_VIDEO = "/dev/video0"
SRT_DEST = "srt://100.71.27.5:5000?mode=caller&latency=200000" 
LOG_FILE = "/app/stream_telemetry_srt.csv"

def start_stream():
    # Filtro drawtext optimizado: 
    # - pts: tiempo del video
    # - gmtime: tiempo real formateado
    # - millisecond: extrae los milisegundos del reloj del sistema
    command = [
        'ffmpeg',
        '-y',
        '-f', 'rawvideo',
        '-pix_fmt', 'bgr24',
        '-s', '640x480',
        '-r', '30',
        '-i', '-', 
        '-vf', "drawtext=fontfile=/usr/share/fonts/dejavu/DejaVuSans.ttf:text='%{localtime\\:%H\\\\\\:%M\\\\\\:%S}.%{eif\\:mod(t*1000,1000)\\:d\\:3}':x=10:y=10:fontsize=24:fontcolor=white:box=1:boxcolor=black@0.5",
        '-c:v', 'libx264',
        '-preset', 'ultrafast',
        '-tune', 'zerolatency',
        '-f', 'mpegts',
        SRT_DEST
    ]

    cap = cv2.VideoCapture(DEV_VIDEO)
    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara")
        return

    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    
    with open(LOG_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'frame_idx', 'proc_time_ms', 'fps_instantaneo'])

        frame_idx = 0
        try:
            while cap.isOpened():
                start_proc = time.perf_counter()
                
                ret, frame = cap.read()
                if not ret: break
                
                process.stdin.write(frame.tobytes())
                
                end_proc = time.perf_counter()
                
                proc_time = (end_proc - start_proc) * 1000
                fps_inst = 1.0 / (end_proc - start_proc) if (end_proc - start_proc) > 0 else 0
                
                if frame_idx % 30 == 0:
                    writer.writerow([time.time(), frame_idx, f"{proc_time:.2f}", f"{fps_inst:.2f}"])
                    f.flush()
                
                frame_idx += 1
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cap.release()
            process.stdin.close()
            process.wait()

if __name__ == "__main__":
    start_stream()