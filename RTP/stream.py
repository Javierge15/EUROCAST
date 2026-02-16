import cv2
import subprocess
import time
import csv
import os

DEV_VIDEO = "/dev/video3"
RTP_DEST = "rtp://127.0.0.1:5004"
LOG_FILE = "stream_telemetry_rtp.csv"

def start_stream():
    # El filtro drawtext usa el reloj local del sistema (localtime)
    # y los milisegundos calculados a partir del tiempo del flujo (t)
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
        '-f', 'rtp',
        '-sdp_file', 'video.sdp',
        RTP_DEST
    ]

    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    cap = cv2.VideoCapture(DEV_VIDEO)
    
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, 'w', newline='') as f: # Cambiado a 'w' para limpiar cada sesión
        writer = csv.writer(f)
        if not file_exists:
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
            print(f"Error durante el stream: {e}")
        finally:
            cap.release()
            process.stdin.close()
            process.wait()

if __name__ == "__main__":
    start_stream()