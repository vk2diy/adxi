import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from fractions import Fraction
from matplotlib.ticker import LogLocator, FuncFormatter

# Get the name of the current script and use it for the output file
script_name = os.path.basename(sys.argv[0])
output_file = os.path.splitext(script_name)[0] + '.png'

# Define the fundamental frequency range and harmonics
f_min, f_max = 900e3, 1.2e6
harmonics = [1/6, 1/5, 1/4, 1/3, 1/2, 2/3, 3/4, 4/5, 5/6, 1, 6/5, 5/4, 4/3, 3/2, 2, 3, 4, 5, 6]

# Define amateur radio bands (name, start_freq, end_freq)
amateur_bands = [
    ("2200m", 135.7e3, 137.8e3),
    ("630m", 472e3, 479e3),
    ("160m", 1.8e6, 2e6),
    ("80m", 3.5e6, 4e6),
    ("40m", 7e6, 7.3e6),
    ("30m", 10.1e6, 10.15e6)
]

# Set up the plot
fig, ax = plt.subplots(figsize=(15, 6))
ax.set_xscale('log')
ax.set_xlim(100e3, 12e6)
ax.set_yticks([])
ax.set_xlabel('Frequency')

# Set x-axis major and minor ticks to include all major logarithmic intervals
ax.xaxis.set_major_locator(LogLocator(base=10.0, numticks=10))  # Major ticks
ax.xaxis.set_minor_locator(LogLocator(base=10.0, subs='auto', numticks=10))  # Minor ticks

# Function to check overlap
def overlaps(range1, range2):
    return range1[0] < range2[1] and range2[0] < range1[1]

# Function to convert float to fraction string
def float_to_fraction_str(f):
    if f == int(f):
        return str(int(f))
    frac = Fraction(f).limit_denominator(10)
    return f"{frac.numerator}/{frac.denominator}"

# Color scaling function
def color_scale(h):
    log_distance = abs(np.log(h))
    opacity = 1.0 - 0.7 * (log_distance / np.log(6))
    return max(opacity, 0.3)

# Plot harmonics as number lines with optimized vertical positioning
harmonic_ranges = [(h * f_min, h * f_max) for h in harmonics]
positions = []
for i, h_range in enumerate(harmonic_ranges):
    position = 0
    while any(overlaps(h_range, harmonic_ranges[j]) for j, pos in positions if pos == position):
        position += 1
    positions.append((i, position))

max_position = max(pos for _, pos in positions)
ax.set_ylim(-1, max_position + 0.1)  # Adjusted to fit the graph

vertical_spacing = 0.4

# Calculate aggregate risk
num_points = 1000
freq_points = np.logspace(np.log10(100e3), np.log10(12e6), num_points)
aggregate_risk = np.zeros(num_points - 1)
for h in harmonics:
    freq_range = (h * f_min, h * f_max)
    aggregate_risk += np.logical_and(freq_points[:-1] >= freq_range[0], freq_points[:-1] <= freq_range[1]) * color_scale(h)

# Plot aggregate risk bar at the top with correct horizontal alignment
risk_mesh = ax.pcolormesh(freq_points, [max_position - 0.5, max_position + 0.1], 
                          [aggregate_risk], cmap='Reds', shading='flat')
ax.text(np.sqrt(100e3 * 12e6), max_position - 0.3, "Aggregate Nominal Interference Risk", 
        ha='center', va='center', fontweight='bold', color='white')

# Add harmonic bands and labels
previous_label = None  # To track the last label
for i, h in enumerate(harmonics):
    freq_range = harmonic_ranges[i]
    position = next(pos for j, pos in positions if j == i) * vertical_spacing
    opacity = color_scale(h)
    color = plt.cm.Reds(opacity)
    ax.plot(freq_range, [position, position], linewidth=4, color=color)
    label = float_to_fraction_str(h) + 'λ'
    ax.text(np.mean(freq_range), position + 0.05, label, ha='center', va='bottom', 
            fontsize=9, color=color, fontweight='bold')

    # Add frequency labels below the aggregate risk bar, avoiding overlaps
    for freq in freq_range:
        if previous_label is None or abs(freq - previous_label) > 100e3:  # 100 kHz threshold
            ax.text(freq, max_position - 1.0, f'{freq / 1e3:.0f} kHz',  # Moved further down
                    ha='center', va='bottom', fontsize=8, color='red', rotation=90)
            previous_label = freq  # Update the last label

# Plot amateur radio bands
for name, start, end in amateur_bands:
    ax.axvspan(start, end, facecolor='blue', alpha=0.2, zorder=1)
    ax.text(np.sqrt(start * end), -0.25, name, ha='center', va='center', rotation=90, fontsize=8)

# Customize x-axis labels
def custom_formatter(x, pos):
    if x >= 1e6:
        return f'{x/1e6:.0f}MHz'
    else:
        return f'{x/1e3:.0f}kHz'

ax.xaxis.set_major_formatter(FuncFormatter(custom_formatter))

plt.title('Harmonic-Affected Frequency Bands and Amateur Radio Bands')
plt.tight_layout()

# Save the figure
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"Graph saved as {output_file}")
