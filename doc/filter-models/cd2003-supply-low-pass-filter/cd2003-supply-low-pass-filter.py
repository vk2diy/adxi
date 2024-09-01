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
    '4700 µF': 4700e-6
}

# Generate frequency points
f = np.logspace(-1, 6, num=1000)  # 0.1 Hz to 1 MHz

# Create the plot
plt.figure(figsize=(12, 7))

# Color cycle for the lines
colors = plt.cm.rainbow(np.linspace(0, 1, len(capacitance_options)))

for (label, C), color in zip(capacitance_options.items(), colors):
    # Calculate magnitude response
    H = transfer_function(f, R, C)
    magnitude_db = 20 * np.log10(np.abs(H))

    # Find -3dB point
    idx_3db = np.argmin(np.abs(magnitude_db + 3))
    f_3db = f[idx_3db]

    # Plot frequency response
    plt.semilogx(f, magnitude_db, label=f'{label} (-3dB: {f_3db:.2f} Hz)', color=color)

    # Mark -3dB point
    plt.plot(f_3db, -3, 'o', color=color, markersize=5)

# Plot settings
plt.grid(True, which="both", ls="-", alpha=0.5)
plt.title('Frequency Response of DC Supply Filter with Different Capacitance')
plt.xlabel('Frequency')
plt.ylabel('Magnitude (dB)')

# Format x-axis labels
def format_freq(x, pos):
    if x >= 1e6:
        return f'{x/1e6:.1f} MHz'
    elif x >= 1e3:
        return f'{x/1e3:.1f} kHz'
    else:
        return f'{x:.1f} Hz'

plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(format_freq))

# Add legend
plt.legend(loc='lower left')

# Set axis limits
plt.ylim(-60, 5)
plt.xlim(0.1, 1e6)

# Save the plot with the same name as the script
script_name = os.path.splitext(os.path.basename(__file__))[0]
plt.savefig(f'{script_name}.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"Graph saved as {script_name}.png")

# Print -3dB frequencies for each configuration
print("\n-3dB frequencies for each configuration:")
for label, C in capacitance_options.items():
    f_3db = 1 / (2 * np.pi * R * C)
    print(f"{label}: {f_3db:.2f} Hz")
