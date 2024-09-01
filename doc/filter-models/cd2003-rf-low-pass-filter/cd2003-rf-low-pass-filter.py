import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqs
import os

# Component values
L = 2.2e-6  # 2.2 µH
C = 620e-12  # 620 pF

# Calculate cutoff frequency
fc = 1 / (2 * np.pi * np.sqrt(L * C))

# Create frequency range (100 kHz to 20 MHz)
f = np.logspace(5, 7.3, num=1000)
w = 2 * np.pi * f

# Calculate transfer function
s = 1j * w
H = 1 / (1 + s**2 * L * C + s * L / 50)  # Assuming 50 ohm source impedance

# Calculate magnitude in dB
mag_db = 20 * np.log10(np.abs(H))

# Create the plot
plt.figure(figsize=(12, 8))
plt.semilogx(f, mag_db)
plt.grid(True, which="both", ls="-", alpha=0.5)

# Set up the axes
plt.xlabel('Frequency')
plt.ylabel('Attenuation (dB)')
plt.title('Low-Pass Filter Frequency Response (2x2.2µH + 620pF)')

# Configure x-axis
plt.xlim(1e5, 2e7)
freq_ticks = [1e5, 2e5, 5e5, 1e6, 2e6, 5e6, 1e7, 2e7]
freq_labels = ['100 kHz', '200 kHz', '500 kHz', '1 MHz', '2 MHz', '5 MHz', '10 MHz', '20 MHz']
plt.xticks(freq_ticks, freq_labels)

# Add vertical line at cutoff frequency
plt.axvline(x=fc, color='r', linestyle='--', label=f'Cutoff Frequency: {fc/1e6:.2f} MHz')

# Add horizontal line at -3 dB
plt.axhline(y=-3, color='g', linestyle=':', label='-3 dB point')

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
