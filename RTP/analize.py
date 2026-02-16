import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('stream_telemetry.csv')
# Ignoramos el primer frame por ser un outlier de inicialización
df = df.iloc[1:] 

plt.figure(figsize=(10, 5))
plt.plot(df['frame_idx'], df['proc_time_ms'], marker='o', linestyle='-', color='orange', label='Tiempo de Procesado')
plt.axhline(y=33.33, color='r', linestyle='--', label='Límite 30 FPS (33.3ms)')

plt.title('Latencia de Procesamiento por Frame (RTP)')
plt.xlabel('Número de Frame')
plt.ylabel('Milisegundos')
plt.legend()
plt.grid(alpha=0.3)
plt.show()