import pandas as pd
import matplotlib.pyplot as plt

# 1. Cargar los datos
# Asegúrate de que el archivo se llame 'datos_tcp.csv' o cambia el nombre aquí
try:
    df = pd.read_csv('TCP_RTT_DATA_1770628374.csv')
except FileNotFoundError:
    print("Error: No se encontró el archivo .csv'.")
    exit()

# 2. Preprocesar el tiempo
# Convertimos el timestamp Unix a tiempo relativo (empezando en 0 segundos)
df['tiempo_relativo'] = df['timestamp'] - df['timestamp'].iloc[0]

# 3. Crear la visualización
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# Gráfica de RTT
ax1.plot(df['tiempo_relativo'], df['rtt_ms'], color='#2ca02c', label='RTT (ms)')
ax1.set_ylabel('Latencia RTT (ms)')
ax1.set_title('Análisis de Tráfico TCP en el Tiempo')
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.legend()

# Gráfica de Inter-arrival
ax2.plot(df['tiempo_relativo'], df['inter_arrival_ms'], color='#1f77b4', label='Inter-arrival (ms)')
ax2.set_xlabel('Tiempo transcurrido (segundos)')
ax2.set_ylabel('Intervalo entre paquetes (ms)')
ax2.grid(True, linestyle='--', alpha=0.7)
ax2.legend()

plt.tight_layout()

# 4. Mostrar estadísticas rápidas en consola
print(f"Estadísticas de RTT:")
print(f"  Promedio: {df['rtt_ms'].mean():.4f} ms")
print(f"  Máximo:   {df['rtt_ms'].max():.4f} ms")
print(f"  Mínimo:   {df['rtt_ms'].min():.4f} ms")

plt.show()