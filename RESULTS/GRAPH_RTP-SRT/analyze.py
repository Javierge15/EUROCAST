import matplotlib.pyplot as plt
import seaborn as sns

# Datos del reloj (Manual Clock Captures)
manual_clock_latency = {
    'RTP LowLat': 95,
    'SRT LowLat': 130,
    'RTP Normal': 160,
    'SRT Normal': 240
}

# Configuración de estilo
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))

names = list(manual_clock_latency.keys())
values = list(manual_clock_latency.values())
# Colores: Verde para los que están bajo el umbral, Rojo para los que no
colors = ['#55A868' if v < 150 else '#C44E52' for v in values]

bars = plt.bar(names, values, color=colors, alpha=0.8)

# Añadimos la "Línea de Seguridad" (Safety Threshold)
plt.axhline(y=150, color='black', linestyle='--', linewidth=2, label='Safety Threshold (150ms)')

# Etiquetas de datos
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 5, f'{yval}ms', 
             ha='center', va='bottom', fontweight='bold', fontsize=12)

plt.title('Total Glass-to-Glass Latency vs. Safety Threshold', fontsize=14)
plt.ylabel('Real Latency (ms)', fontsize=12)
plt.ylim(0, 300)
plt.legend()

plt.tight_layout()
plt.savefig('total_latency_safety_margin.png', dpi=300)
print("Saved: total_latency_safety_margin.png")