import numpy as np
import matplotlib.pyplot as plt
import os

# Constants
R = 10e3  # Example resistance value in ohms (adjust as needed)
C1 = 100e-9  # 100nF capacitor value in Farads
C2 = 470e-9  # 470nF capacitor value in Farads

# Frequency range
frequencies = np.logspace(1, 6, 500)  # from 10 to 10^6 Hz, logarithmically spaced

# Calculate magnitude of impedance for each capacitor combination
Z1 = 1 / (1j * 2 * np.pi * frequencies * C1)  # Impedance of C1
Z2 = 1 / (1j * 2 * np.pi * frequencies * C2)  # Impedance of C2

# Total impedance in series
Z_total1 = R + Z1
Z_total2 = R + Z2

# Calculate magnitude of voltage divider transfer function
gain1 = np.abs(Z1 / Z_total1)
gain2 = np.abs(Z2 / Z_total2)

# Plotting
plt.figure(figsize=(10, 6))

plt.semilogx(frequencies, 20 * np.log10(gain1), label='100nF Capacitor')
plt.semilogx(frequencies, 20 * np.log10(gain2), label='470nF Capacitor')

plt.title('Frequency Response of Capacitors in Series with 10kΩ Resistor')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Gain (dB)')
plt.grid(True)
plt.legend()

plt.ylim(-40, 0)  # Limit the y-axis to -40 dB to 0 dB for better visualization

plt.tight_layout()

# Save plot as PNG with language-specific suffix
script_name = os.path.basename(__file__).split('.')[0]  # Get script name without extension
suffix = f'.png'
output_file = f'{script_name}{suffix}'
plt.savefig(output_file)
    
# Close plot to release memory
plt.close()


