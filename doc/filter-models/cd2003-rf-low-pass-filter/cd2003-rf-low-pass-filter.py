import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import os

# Component values
L = 2.2e-6  # 2.2 µH
C1 = 620e-12  # 620 pF (current configuration)
C2 = 440e-12  # 440 pF (2 x 220pF in parallel)
C3 = 660e-12  # 660 pF (3 x 220pF in parallel)
C4 = 990e-12  # 990 pF (3 x 330pF in parallel)

# Create frequency range (100 kHz to 20 MHz)
f = np.logspace(5, 7.3, num=1000)
w = 2 * np.pi * f

# Calculate transfer functions
def calc_H(L, C, w):
    s = 1j * w
    return 1 / (1 + s**2 * L * C + s * L / 50)

H1, H2, H3, H4 = map(calc_H, [L]*4, [C1, C2, C3, C4], [w]*4)

# Calculate magnitudes in dB
mag_db1, mag_db2, mag_db3, mag_db4 = map(lambda H: 20 * np.log10(np.abs(H)), [H1, H2, H3, H4])

# Find -3dB points
def find_3db_point(f, mag_db):
    interp = interp1d(mag_db, f, kind='linear')
    return interp(-3)

fc1, fc2, fc3, fc4 = map(find_3db_point, [f]*4, [mag_db1, mag_db2, mag_db3, mag_db4])

# Define colors for each configuration
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

# Create the plot
plt.figure(figsize=(12, 8))
plt.semilogx(f, mag_db1, color=colors[0], label='620pF')
plt.semilogx(f, mag_db2, color=colors[1], label='440pF (2x220pF)')
plt.semilogx(f, mag_db3, color=colors[2], label='660pF (3x220pF)')
plt.semilogx(f, mag_db4, color=colors[3], label='990pF (3x330pF)')
plt.grid(True, which="both", ls="-", alpha=0.5)

# Set up the axes
plt.xlabel('Frequency')
plt.ylabel('Attenuation (dB)')
plt.title('Low-Pass Filter Frequency Response Comparison')

# Configure x-axis
plt.xlim(1e5, 2e7)
freq_ticks = [1e5, 2e5, 5e5, 1e6, 2e6, 5e6, 1e7, 2e7]
freq_labels = ['100 kHz', '200 kHz', '500 kHz', '1 MHz', '2 MHz', '5 MHz', '10 MHz', '20 MHz']
plt.xticks(freq_ticks, freq_labels)

# Add vertical lines at -3dB points
for fc, color, label in zip([fc1, fc2, fc3, fc4], colors, ['620pF', '440pF', '660pF', '990pF']):
    plt.axvline(x=fc, color=color, linestyle='--', label=f'-3dB point ({label}): {fc/1e6:.2f} MHz')

# Add horizontal line at -3 dB
plt.axhline(y=-3, color='k', linestyle=':', label='-3 dB line')

plt.legend()
plt.tight_layout()

# Get the script's filename without extension
script_name = os.path.splitext(os.path.basename(__file__))[0]

# Save the plot as a PNG file with the same name as the script
output_filename = f"{script_name}.png"
plt.savefig(output_filename, dpi=300, bbox_inches='tight')
print(f"Graph saved as {output_filename}")

# Optionally, you can still display the plot if running interactively
# plt.show()
