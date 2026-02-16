import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 1. Cargar los datos
# Asegúrate de que los archivos estén en la misma carpeta que el script
files = {
    'UDP Stopped': 'UDP_STOPPED_.csv',
    'TCP Stopped': 'TCP_STOPPED_.csv',
    'UDP Moving': 'UDP_MOVING.csv',
    'TCP Moving': 'TCP_MOVING.csv'
}

dataframes = []
for label, path in files.items():
    df = pd.read_csv(path)
    df['Scenario'] = label
    # Separamos el protocolo y el estado para facilitar filtros después
    df['Protocolo'] = 'UDP' if 'UDP' in label else 'TCP'
    df['Estado'] = 'Parado' if 'Stopped' in label else 'Movimiento'
    dataframes.append(df)

all_data = pd.concat(dataframes, ignore_index=True)

# 2. Configuración estética para Paper
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 12})

# --- GRÁFICA 1: BOXPLOT COMPARATIVO (RTT) ---
plt.figure(figsize=(10, 6))
sns.boxplot(x='Scenario', y='rtt_ms', data=all_data, palette='Set2')
plt.title('RTT Latency Comparison')
plt.ylabel('RTT (ms)')
plt.xlabel('')
plt.savefig('boxplot_rtt.png', dpi=300)
plt.show()

# --- GRÁFICA 2: SERIE TEMPORAL (Comparación Moving) ---
plt.figure(figsize=(12, 5))
moving_data = all_data[all_data['Estado'] == 'Movimiento']
for proto in ['UDP', 'TCP']:
    subset = moving_data[moving_data['Protocolo'] == proto]
    # Usamos seq para el eje X para que sean comparables
    plt.plot(subset['seq'], subset['rtt_ms'], label=f'{proto} Moving', alpha=0.7)

plt.title('RTT Evolution During Movement')
plt.xlabel('Packet Sequence')
plt.ylabel('RTT (ms)')
plt.legend()
plt.savefig('timeseries_moving.png', dpi=300)
plt.show()

# --- GRÁFICA 3: ANÁLISIS DE JITTER (Histograma) ---
# Calculamos el Jitter como el valor absoluto de la diferencia entre RTTs consecutivos
all_data['jitter'] = all_data.groupby('Scenario')['rtt_ms'].diff().abs()

plt.figure(figsize=(10, 6))
sns.kdeplot(data=all_data, x='jitter', hue='Scenario', fill=True, common_norm=False)
plt.title('Jitter Distribution')
plt.xlabel('Jitter (ms)')
plt.ylabel('Density')
plt.xlim(0, 20) # Limitamos para ver mejor la zona crítica
plt.savefig('jitter_distribution.png', dpi=300)
plt.show()

# --- 3. CÁLCULO DE MÉTRICAS PARA LA TABLA DEL PAPER ---
metrics = all_data.groupby('Scenario')['rtt_ms'].agg([
    ('Media', 'mean'),
    ('Desv. Est.', 'std'),
    ('Mín', 'min'),
    ('Máx', 'max'),
    ('P99 (Percentil 99)', lambda x: x.quantile(0.99))
]).round(3)

print("\n--- MÉTRICAS PARA LA TABLA DEL PAPER ---")
print(metrics)

# Guardar métricas a CSV
metrics.to_csv('metricas_resultado.csv')