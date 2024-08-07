import numpy as np
import matplotlib.pyplot as plt
import gettext
import os

# Define translations for English, Dutch, and German
translations = {
    'en': {
        'title': 'Frequency Response of Capacitor in Series',
        'xlabel': 'Frequency (MHz)',
        'ylabel': 'Magnitude (dB)',
        'legend_title': 'Capacitor Value',
        '2m_band': '2m Band (144-148 MHz)',
        '10m_band': '10m Band (28-30 MHz)',
        '20m_band': '20m Band (14-14.35 MHz)',
        '40m_band': '40m Band (7-7.3 MHz)',
        '80m_band': '80m Band (3.5-4 MHz)',
    },
    'nl': {
        'title': 'Frequentieresponsie van Condensator in Serie',
        'xlabel': 'Frequentie (MHz)',
        'ylabel': 'Magnitude (dB)',
        'legend_title': 'Condensator Waarde',
        '2m_band': '2m Band (144-148 MHz)',
        '10m_band': '10m Band (28-30 MHz)',
        '20m_band': '20m Band (14-14.35 MHz)',
        '40m_band': '40m Band (7-7.3 MHz)',
        '80m_band': '80m Band (3.5-4 MHz)',
    },
    'de': {
        'title': 'Frequenzantwort eines Kondensators in Serie',
        'xlabel': 'Frequenz (MHz)',
        'ylabel': 'Magnitude (dB)',
        'legend_title': 'Kondensator Wert',
        '2m_band': '2m Band (144-148 MHz)',
        '10m_band': '10m Band (28-30 MHz)',
        '20m_band': '20m Band (14-14.35 MHz)',
        '40m_band': '40m Band (7-7.3 MHz)',
        '80m_band': '80m Band (3.5-4 MHz)',
    }
}

# Select languages for which to generate plots
languages = ['en', 'nl', 'de']

# Frequency range (Hz), from DC to beyond 2m band maximum carrier frequency
frequencies = np.linspace(0, 160e6, 1000)  # 0 Hz to 160 MHz

# Capacitor values to simulate (F)
capacitor_values = [1e-9, 10e-9, 100e-9, 1e-6]  # 1nF, 10nF, 100nF, 1uF

# Calculate the magnitude response for each capacitor value
for language in languages:
    # Activate translation based on selected language
    gettext_translation = gettext.translation('base', localedir=None, languages=[language], fallback=True)
    _ = gettext_translation.gettext
    
    # Initialize lists to store data
    magnitude_responses = []
    labels = []

    # Calculate the magnitude response for each capacitor value
    for C in capacitor_values:
        # Calculate impedance magnitude |Z| = 1 / (2 * pi * f * C)
        impedance_magnitude = 1 / (2 * np.pi * frequencies * C)

        # Convert impedance to magnitude in dB
        magnitude_dB = 20 * np.log10(impedance_magnitude)

        # Store magnitude response
        magnitude_responses.append(magnitude_dB)

        # Create label for legend
        if C < 1e-6:
            labels.append(f'{C*1e9:.0f} nF')
        else:
            labels.append(f'{C*1e6:.0f} uF')

    # Plotting
    plt.figure(figsize=(10, 6))
    for idx, response in enumerate(magnitude_responses):
        plt.plot(frequencies / 1e6, response, label=labels[idx])

    # Shade frequency bands
    plt.axvspan(144, 148, color='gray', alpha=0.3, label=_(translations[language]['2m_band']))
    plt.axvspan(28, 30, color='blue', alpha=0.3, label=_(translations[language]['10m_band']))
    plt.axvspan(14, 14.35, color='green', alpha=0.3, label=_(translations[language]['20m_band']))
    plt.axvspan(7, 7.3, color='orange', alpha=0.3, label=_(translations[language]['40m_band']))
    plt.axvspan(3.5, 4, color='red', alpha=0.3, label=_(translations[language]['80m_band']))

    plt.xlabel(_(translations[language]['xlabel']))
    plt.ylabel(_(translations[language]['ylabel']))
    plt.title(_(translations[language]['title']))
    plt.grid(True)
    plt.xlim(0, frequencies[-1] / 1e6)
    plt.ylim(-60, 10)  # Adjusted y-axis limits for clarity
    plt.legend(title=_(translations[language]['legend_title']), loc='lower center')
    plt.tight_layout()

    # Save plot as PNG with language-specific suffix
    script_name = os.path.basename(__file__).split('.')[0]  # Get script name without extension
    suffix = f'-{language}.png'
    output_file = f'{script_name}{suffix}'
    plt.savefig(output_file)
    
    # Close plot to release memory
    plt.close()

