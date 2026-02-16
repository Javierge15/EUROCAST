import pandas as pd
import matplotlib.pyplot as plt

# Cargar los datos
df = pd.read_csv("UDP_RTT_DATA_1770628005.csv")

# Filtrar pérdidas para estadísticas
success = df[df['status'] == 'OK']
losses = df[df['status'] == 'LOST']

print(f"Estadísticas de la prueba:")
print(f"Total paquetes: {len(df)}")
print(f"Pérdidas: {len(losses)} ({len(losses)/len(df)*100:.2f}%)")
print(f"RTT Medio: {success['rtt_ms'].mean():.3f} ms")
print(f"Jitter (Std Dev): {success['rtt_ms'].std():.3f} ms")

# Graficar RTT a lo largo del tiempo
plt.figure(figsize=(12, 6))
plt.plot(success['seq'], success['rtt_ms'], label='UDP RTT (ms)', color='blue', linewidth=1)
plt.scatter(losses['seq'], [0]*len(losses), color='red', label='Packet Loss', marker='x')

plt.title('Latencia UDP en Tiempo Real (Entorno Móvil)')
plt.xlabel('Número de Secuencia')
plt.ylabel('RTT (ms)')
plt.legend()
plt.grid(True)
plt.show()