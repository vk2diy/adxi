import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from matplotlib.ticker import FuncFormatter

# Inline translations keyed by language code
translations = {
    'en': {
        'title': 'Frequency Response of Low-Pass Pi Filter',
        'xlabel': 'Frequency (Hz)',
        'ylabel': 'Gain (dB)'
    },
    'nl': {
        'title': 'Frequentierespons van laagdoorlaat Pi-filter',
        'xlabel': 'Frequentie (Hz)',
        'ylabel': 'Versterking (dB)'
    },
    'de': {
        'title': 'Frequenzgang des Tiefpass-Pi-Filters',
        'xlabel': 'Frequenz (Hz)',
        'ylabel': 'Verstärkung (dB)'
    }
}

# Function to retrieve translations based on language code
def _(text, language_code='en'):
    if language_code in translations and text in translations[language_code]:
        return translations[language_code][text]
    return text  # Default to returning the text itself if translation not found

# Define component values
C1 = 100e-6  # 100uF
C2 = 100e-9  # 100nF
L = 1000e-6   # 1000uH
C3 = 10e-6    # 10uF
C4 = 100e-9   # 100nF

# Calculate transfer function of the low-pass pi filter
def low_pass_filter_transfer_function(s):
    return C4 / (C1 * C2 * C3 * s**2 + (C1 * C2 + C2 * C3 + C1 * C3 + C1 * C4 + C2 * C4) * s + 1)

# Generate frequencies for plotting
frequencies = np.linspace(1, 10e6, num=10000)  # Frequency range from 1 Hz to 10 MHz
omega = 2 * np.pi * frequencies
s = 1j * omega

# Calculate transfer function H(jω)
H = low_pass_filter_transfer_function(s)

# Plotting and saving for each language
script_name = os.path.splitext(os.path.basename(__file__))[0]

for language_code in translations:
    plt.figure(figsize=(10, 6))
    plt.semilogx(frequencies, 20 * np.log10(np.abs(H)))
    plt.title(_(translations[language_code]['title'], language_code))
    plt.xlabel(_(translations[language_code]['xlabel'], language_code))
    plt.ylabel(_(translations[language_code]['ylabel'], language_code))
    plt.grid(True)
    plt.tight_layout()

    # Format frequency axis to display Hz
    formatter = FuncFormatter(lambda x, _: f'{int(x):,} Hz')
    plt.gca().xaxis.set_major_formatter(formatter)

    # Save plot with appropriate filename
    output_filename = f'{script_name}-{language_code}.png'
    plt.savefig(output_filename)

    # Close plot to prevent displaying it
    plt.close()

