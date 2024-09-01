import numpy as np
import matplotlib.pyplot as plt
import os

def transfer_function(f, R, C):
    s = 2j * np.pi * f
    return 1 / (1 + s * R * C)

# Filter components
R = 10  # 10 ohms

# Different capacitance options
capacitance_options = {
    '470 µF': 470e-6,
    '2x470 µF (940 µF)': 2 * 470e-6,
    '3x470 µF (1410 µF)': 3 * 470e-6,
    '4x470 µF (1880 µF)': 4 * 470e-6,
    '4700 µF': 4700e-6,
    '2x470µF + 100µF + 10µF (1050 µF)': 2 * 470e-6 + 100e-6 + 10e-6
}

# Load current (in Amperes)
I_load = 10.5e-3  # 10.5 mA
# Ripple frequency (in Hz)
f_ripple = 3e8 / 40  # Speed of light / wavelength = 7.5 MHz

# Generate frequency points
f = np.logspace(-1, 5, num=1000)  # 0.1 Hz to 100 kHz

# Create a combined figure with subplots
fig, axs = plt.subplots(2, 1, figsize=(12, 12), gridspec_kw={'height_ratios': [2, 1]})

# Define colors for each configuration
colors = plt.cm.viridis(np.linspace(0, 1, len(capacitance_options)))

# Ripple voltage storage
ripple_voltages = []

# Loop through each capacitance option
for (label, C), color in zip(capacitance_options.items(), colors):
    # Calculate magnitude response
    H = transfer_function(f, R, C)
    magnitude_db = 20 * np.log10(np.abs(H))
    phase = np.angle(H, deg=True)

    # Plot magnitude response
    axs[0].semilogx(f, magnitude_db, label=f'{label} Magnitude', color=color)

    # Plot phase response with dashed line
    axs[0].semilogx(f, phase, linestyle='--', label=f'{label} Phase', color=color)

    # Mark -3dB point
    idx_3db = np.argmin(np.abs(magnitude_db + 3))
    axs[0].plot(f[idx_3db], magnitude_db[idx_3db], 'o', color=color, markersize=5)  # Point for -3dB

    # Mark 45-degree point
    idx_45 = np.argmin(np.abs(phase + 45))
    axs[0].plot(f[idx_45], phase[idx_45], 'o', color=color, markersize=5)  # Point for 45 degrees

    # Calculate ripple voltage for this capacitance
    ripple_voltage = I_load / (f_ripple * C)
    ripple_voltages.append(ripple_voltage)

# Plot settings for Bode plot
axs[0].grid(True, which="both", ls="-", alpha=0.5)
axs[0].set_title('Bode Plot of DC Supply Filter with Different Capacitance')
axs[0].set_ylabel('Magnitude (dB) / Phase (degrees)')

# Format x-axis labels
def format_freq(x, pos):
    if x >= 1e5:
        return f'{x/1e6:.1f} MHz'
    elif x >= 1e3:
        return f'{x/1e3:.1f} kHz'
    else:
        return f'{x:.1f} Hz'

axs[0].xaxis.set_major_formatter(plt.FuncFormatter(format_freq))

# Add legend to the top right
axs[0].legend(loc='upper right', fontsize='small')

# Set y-axis limits for magnitude and phase
axs[0].set_ylim(-60, 5)
axs[0].set_xlim(0.1, 100e3)  # Limit the x-axis to 100 kHz

# Plot settings for ripple voltage (horizontal bar graph)
axs[1].barh(list(capacitance_options.keys()), ripple_voltages, color=colors)
axs[1].set_title('Ripple Voltage for Different Capacitor Configurations')
axs[1].set_xlabel('Ripple Voltage (V)')
axs[1].set_ylabel('Capacitance Configuration')
axs[1].grid(axis='x')

# Adjust layout
plt.tight_layout()

# Save the combined plot
script_name = os.path.splitext(os.path.basename(__file__))[0]
plt.savefig(f'{script_name}_combined.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"Combined graph saved as {script_name}_combined.png")
