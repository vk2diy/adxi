# Quadrature Sampling Detection

Quadrature sampling detection (aka 'quadrature detection' or 'quadrature detector') circuits are used in signal processing to extract in-phase (`I`) and quadrature (`Q`) components from an input signal.


```

input signal ---> QSD ---> in-phase component (I) ------> further processing ---> output
                   |                                       ^
                   `-----> quadrature component (Q) -------'
```

## Types of QSD

There are several types of quadrature sampling detection circuits, each with its own advantages and implementation methods:

### Analog Quadrature Detector

This traditional method uses analog circuits to perform quadrature detection:

 * It multiplies the incoming signal with two local oscillators that are 90 degrees out of phase.
 * The resulting `I` and `Q` signals are then low-pass filtered to remove high-frequency components.
 * Advantages: Can handle high-frequency signals.
 * Disadvantages: Requires precise analog components and may suffer from imbalances.

### Digital Quadrature Detector

Modern transceivers often implement quadrature detection digitally:

 * The incoming analog signal is first converted to digital form using an analog-to-digital converter (ADC).
 * Digital multiplication and filtering are then used to extract `I` and `Q` components.
 * Advantages: More flexible, can be easily reconfigured in software.
 * Disadvantages: May be limited by ADC sampling rate for very high-frequency signals.

### Tayloe Quadrature Detector

This is a unique type of quadrature sampling detector:

 * It uses a switching mechanism to sample the input signal at four points, 90 degrees apart.
 * The sampled values are integrated using capacitors to produce `I` and `Q` outputs.
 * Advantages:
   * Near unity gain (much better than a diode mixer/detector, which will be worse than –6dB. QSD uses near peak detection instead of RMS and there is not a sum product which otherwise is thrown away and wasted)
   * Large dynamic range (primarily a function of operating voltage of the analog switches)
   * Simple design (no tuned circuits, agnostic to RF below the maximum switching rate of the analog switch input, easily adjusted, 
   * Built in front end selectivity (eg. if input = 10Mhz and filter knee = 1KHz (need to double this for the calculation), then front end selectivity `Q` = 10Mhz/2KHz = 5000)
 * Disadvantages:
   * Performance may degrade at very high frequencies.
   * Needs to be driven by a Local Oscillator (LO) at 4X the desired reception frequency. For example, to listen to a 10MHz station you need to generate 40MHz and divide into 4 (90 degree phased) clock signals).
   * Needs to be driven by a square wave – which introduces harmonic detecting and spurious signals. Front end selectivity will mitigate this.
   * The gain, bandwidth and noise of the detector are very sensitive to antenna impedance matching. Requires a well-defined RF input impedance for best performance.
   * AM leakage can be present, although it is much better than traditional product detectors (worse with huge resonant antennas)
   * Makes a beat note, so AM detection requires careful tuning with a really stable oscillator or requires tuning above 20KHz, band pass filtering, and summing to full wave rectified output (absolute value circuit) to create AM detection. Alternatively, you can A/D convert and use DSP signal processing.

At first glance, this circuit appears to be to be a switching mixer used as a product detector. This is not quite accurate. It really is a sampling detector which generates a difference beat(when LO is slightly out of tune with the incoming signal), but not a sum product. The very basic idea is to switch on and off  a RF input into an audio range low pass RC filter and detect (integrate) the difference beat frequency or modulation envelope, when exactly at zero beat. A simple diode detector is analagous to some degree – the difference is; it self switches so it is always perfectly synchronized to zero beat. Also, a diode only switches on for a portion of  a half cycle, hence there are losses.

The fact this is a detector (not a mixer) and that it is quadrature sampling leads to two very important benefits. One, I and Q signals are easily obtained. This allows sideband rejection via an analog all pass filter or DSP processing. Second, it provides near unity gain (since you have no sum product, you do not lose half of your energy in detection, aswell, you detect at 90% of peak not RMS).

References:
 * [this site](https://circuitsalad.com/2013/12/30/my-phasing-receiver-is-a-success/)

### Second Order Quadrature Detector

This method is particularly useful for narrowband signals:

 * It samples the input signal at a rate much lower than the carrier frequency.
 * In-phase samples are taken at intervals of `l/(2f0)`, where `f0` is the carrier frequency and `l` is an integer.
 * Quadrature samples are taken after a delay of `1/(4f0)` relative to the in-phase samples.
 * Advantages: Allows for a much lower sampling rate compared to the carrier frequency.
 * Disadvantages: May introduce some approximation errors for wider bandwidth signals.

### Interleaved Quadrature Detector

This method is optimized for efficient digitization:

 * It uses interleaved in-phase and quadrature clock pulses at twice the carrier frequency (or a subharmonic).
 * The interleaved clock is used as an external clock for digitization of the phase-modulated carrier.
 * Advantages: Requires sampling at only twice the information bandwidth rather than twice the carrier frequency.
 * Disadvantages: Requires precise timing control for the interleaved clock signals.

Each of these quadrature sampling detection methods has its own strengths and is suited for different applications depending on factors such as signal bandwidth, carrier frequency, and required precision.
