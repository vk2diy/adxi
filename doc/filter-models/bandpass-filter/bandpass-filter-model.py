import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import TransferFunction, bode

# Define the components values (re-verified)
C1 = 100e-9  # 100nF
R1 = 1e6     # 1MΩ
R2 = 4.7e3   # 4.7kΩ
R3 = 10e3    # 10kΩ
C2 = 10e-9   # 10nF
R4 = 10e3    # 10kΩ
C3 = 10e-9   # 10nF

# Transfer function components re-evaluated
numerator = [C1 * R1 * R3 * C2, 0, 0]
denominator = [
    C1 * R1 * R3 * R4 * C2 * C3,
    (R1 + R2 + R3) * C1 * C3 * R4,
    (R3 + R4) * C1 + (R1 + R2) * C3 + R3 * C2,
    1
]

# Create Transfer Function
system = TransferFunction(numerator, denominator)

# Frequency range for analysis
frequencies = np.logspace(1, 6, 1000)  # 10 Hz to 1 MHz
w = 2 * np.pi * frequencies  # Angular frequency

# Calculate the frequency response
w, mag, phase = bode(system, w)

# Interpolation for -3dB points
def find_cutoff_frequency(frequencies, mag_db, target_db=-3):
    idx = np.where(np.diff(np.sign(mag_db - target_db)))[0]
    if len(idx) > 0:
        idx = idx[0]
        f1, f2 = frequencies[idx], frequencies[idx + 1]
        m1, m2 = mag_db[idx], mag_db[idx + 1]
        cutoff_freq = f1 + (f2 - f1) * (target_db - m1) / (m2 - m1)
        return cutoff_freq
    return None

low_cutoff_freq = find_cutoff_frequency(frequencies, mag, -3)
high_cutoff_freq = find_cutoff_frequency(frequencies[::-1], mag[::-1], -3)

# Generate the plot
plt.figure(figsize=(10, 7))

# Magnitude plot
plt.subplot(2, 1, 1)
plt.plot(frequencies, mag)
plt.title('ADX Bandpass Filter Frequency Response')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.axhline(-3, color='r', linestyle='--', label='-3 dB Point')

# Indicate specific cutoff frequencies
if low_cutoff_freq:
    plt.axvline(low_cutoff_freq, color='g', linestyle='--', label=f'Low Cutoff: {low_cutoff_freq:.1f} Hz')
if high_cutoff_freq:
    plt.axvline(high_cutoff_freq, color='b', linestyle='--', label=f'High Cutoff: {high_cutoff_freq:.1f} Hz')

plt.legend(loc='best')

# Convert frequency axis to human-readable Hz suffixes
plt.xscale('log')
freq_ticks = [10, 100, 1e3, 10e3, 100e3, 1e6]
freq_labels = ['10 Hz', '100 Hz', '1 kHz', '10 kHz', '100 kHz', '1 MHz']
plt.xticks(freq_ticks, freq_labels)

# Phase plot
plt.subplot(2, 1, 2)
plt.plot(frequencies, phase)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Phase (degrees)')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.xscale('log')
plt.xticks(freq_ticks, freq_labels)

# Adjust layout
plt.tight_layout()

# Save the figure
script_name = __file__
output_name = script_name.replace('.py', '.png')
plt.savefig(output_name)
