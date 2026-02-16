import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 1. FILE CONFIGURATION
# Mapping the new telemetry files
files = {
    'WebSockets Moving': 'telemetry_websockets_MOVING.csv',
    'WebSockets Stopped': 'telemetry_websockets_STOPPED_POS.csv',
    'WebRTC Moving': 'telemetry_webrtc_MOVING.csv',
    'WebRTC Stopped': 'telemetry_webrtc_STOPPED_POS.csv'
}

dataframes = []
for label, path in files.items():
    try:
        df = pd.read_csv(path)
        df['Test_Case'] = label
        df['Technology'] = 'WebSockets' if 'websockets' in path else 'WebRTC'
        df['Status'] = 'Moving' if 'MOVING' in path else 'Stopped'
        dataframes.append(df)
    except FileNotFoundError:
        print(f"Warning: File {path} not found.")

all_telemetry = pd.concat(dataframes, ignore_index=True)

# 2. STYLE SETTINGS
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 12, 'figure.autolayout': True})

# --- GRAPH 1: LATENCY BOXPLOT (WebRTC vs WebSockets) ---
plt.figure(figsize=(10, 6))
sns.boxplot(x='Test_Case', y='latency_ms', hue='Test_Case', data=all_telemetry, palette='Set1', legend=False)
plt.title('Latency Comparison')
plt.ylabel('Latency (ms)')
plt.xlabel('')
plt.xticks(rotation=15)
plt.savefig('telemetry_latency_boxplot.png', dpi=300)

# --- GRAPH 2: JITTER DENSITY PLOT (KDE) ---
# Using the KDE style you liked for the previous analysis
plt.figure(figsize=(10, 6))
sns.kdeplot(
    data=all_telemetry, 
    x='jitter_ms', 
    hue='Test_Case', 
    fill=True, 
    common_norm=False, 
    palette='magma', 
    alpha=0.4
)
plt.title('Jitter Distribution')
plt.xlabel('Jitter (ms)')
plt.ylabel('Density')
plt.xlim(0, 60) # Adjusted based on typical telemetry jitter
plt.savefig('telemetry_jitter_density.png', dpi=300)

# --- 3. METRICS GENERATION FOR THE PAPER ---
# Calculating key statistics for your results table
metrics = all_telemetry.groupby('Test_Case')['latency_ms'].agg([
    ('Mean Latency', 'mean'),
    ('Std Dev (Jitter)', 'std'),
    ('Max Latency', 'max'),
    ('P99 Latency', lambda x: x.quantile(0.99))
]).round(2)

print("\n" + "="*50)
print("TELEMETRY FRAMEWORK ANALYSIS - RESULTS")
print("="*50)
print(metrics)
print("="*50)

# Save to CSV
metrics.to_csv('telemetry_framework_results.csv')