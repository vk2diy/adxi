# SWR Monitor and Power Metering

One of the main ways that amateur radio operators traditionally evaluate their antenna system is by measuring the __[standing wave ratio (SWR)](https://en.wikipedia.org/wiki/Standing_wave_ratio)__ (also known as VSWR or "voltage standing wave ratio") of the antenna system.

The __SWR__ is simply the ratio of power forward (being sent out) to reverse (being reflected back), ie:

 * Github: $$SWR = \frac{P_{forward}}{P_{reverse}}$$
 * Unicode/HTML: <code>SWR = P<sub>forward</sub> ÷ P<sub>reverse</sub></code>

## How it's normally done

The traditional way to build an SWR monitor is via a __directional coupler__ ([wikipedia](https://en.wikipedia.org/wiki/Power_dividers_and_directional_couplers)), which is a device that provides distinct feeds for each direction.

While you can purchase SMT directional couplers, they are expensive and relatively hard to find.

## How we're doing it

It turns out they often provide a far higher signal quality than is required for pure power metering and SWR metering.

So instead, we "roll our own" with the following strategy:

 * Provide two different signal paths from the power amplifier (PA) output that is headed toward the antenna system (ANT)
 * In each signal path:
   * Attenuate the power to a reduced level
   * Provide diodes to ensure power only flows in one direction
   * Provide some protection against over-voltage
   * Feed the resulting signal to the [microcotroller unit (MCU)](../mcu/) ("brain") on a pin with an analog to digital converter (ADC) in order to sample the level

This should allow us to basically obtain power levels for each direction, and to simply compute the SWR.

### Diode selection

There are two aspects to the diode selection for this circuit, power dissipation and speed.

Due to the leading resistor reducing current, power dissipation is probably not something to worry about but we would prefer a larger figure just for safety.

Speed is a significant concern.

The diodes must be fast enough to provide switching at the required frequencies, which at the high end (70cm band) are around 440MHz - quite fast.

A common rule of thumb is that the maximum usable frequency for a diode is approximately:

$$f_{max} \approx \frac{0.35}{t_{rr}}$$ (or, as Unicode: `f_max ≈ 0.35 / t_rr`)

 * Where:
   * $$t_{rr}$$ (`t_rr`) is the diode's "reverse recovery time" from the datasheet.

This rule of thumb is based on the 0.35 factor, which corresponds to sampling approximately 2.86 times per cycle (1/0.35 ≈ 2.86). This is higher than the hard limit recommended by [Nyquist-Shannon sampling theorem](https://en.wikipedia.org/wiki/Nyquist%E2%80%93Shannon_sampling_theorem) of two times per cycle to avoid [aliasing](https://en.wikipedia.org/wiki/Aliasing).

We had originally chosen to use `1N4148WS` however this has a 4ns `t_rr` which limits frequency to around 100MHz.

By changing the diode to `1N5711W-7-F` with a 1ns `t_rr` we now hope to see better performance at higher frequencies.

By choosing `1N5711W-7-F` (SOD-123 package) instead of `1N5711WS-7-F` (SOD-323 package) we can obtain 3x the power dissipation for "free" (no effective cost difference, just board space).

#### Ideal case calculation

We calculate that the ideal switching frequency would be 0.8ns, as follows:

$$t_{rr} \approx \frac{0.35}{f_{target}}$$ (or, as Unicode: `t_rr ≈ 0.35 / f_target`)

So in our case:

$$t_{rr} \approx \frac{0.35}{440MHz} \approx 0.8ns$$ (or, as Unicode: `t_rr ≈ 0.35 / 440MHz ≈ 0.8ns`)

A hard limit of two (not practically used as this is asking for problems) would substitute 0.5 instead of 0.35, so:

$$t_{rr} \approx \frac{0.5}{f_{target}}$$ (or, as Unicode: `t_rr ≈ 0.5 / f_target`)

So in our case:

$$t_{rr} \approx \frac{0.5}{440MHz} \approx 1.14ns$$ (or, as Unicode: `t_rr ≈ 0.5 / 440MHz ≈ 1.14ns`)

You can see that 1ns falls within the hard limit but is rather close. Probably a non-issue since we just want low frequency sampling of a general rate of FWP/RVP and thus calculate SWR and we can potentially average the last few readings in the firmware in order to effectively reduce impact of any sampling rate related abberations.

More explicitly:

 * Let's start with the basic equation:
   * $$t_{rr} \approx 0.5 / f$$
   * Where:
     * `t` is time in seconds
     * `f` is frequency in Hz
     * 0.5 is the "sample length as a proportion of the cycle" factor we're using (derived from the Nyquist theorem), with 0.5 meaning "two samples per cycle", and could also be expressed as `1 / samples_per_cycle`, where `samples_per_cycle` is `2`.
   * Our result will be a time period in seconds
 * We have f = 440MHz, but we need to convert this to Hz:
   * 440MHz = 440,000,000 Hz
 * Now we can plug this into our equation:
   * $$t_{rr} \approx \frac{0.5}{440,000,000 Hz}$$
 * Perform the division:
   * $$t_{rr} \approx 0.00000000113636363636 seconds$$
 * Convert to nanoseconds:
   * $$0.00000000113636363636 seconds \times 1,000,000,000 ns/s = 1.13636363636 ns$$
 * Thus, rounded to two decimal places:
   * $$t_{rr} \approx \frac{0.5}{440 MHz} \approx 1.14 ns$$

Alternatively:

$$t_{cycle length in seconds} = \frac{1 second}{Hz}

t_{cycle length in seconds} = \frac{1 second}{440,000,000 Hz}

\therefore t_{cycle length in seconds} = 0.00000000113636363636 seconds

t_{cycle length in nanoseconds} = t_{cycle length in seconds} \times 1,000,000,000 ns/s

\therefore t_{cycle length in nanoseconds} = 0.00000000113636363636 \times 1,000,000,000 = 1.13636363636 ns \approx 1.14ns$$

## Conclusion

We should have created a directional sampling circuit with adequate speed and characteristics to obtain forward power and reverse power at the [microcontroller unit (MCU)](../mcu/). From these, we can calculate SWR (standing wave ratio).

The acquisition of this information is of significant use, both:
 * when tuning the antenna system; and
 * to prevent damage to the system in situations like:
   * if there is no antenna plugged in
   * if the wrong antenna system is plugged in
   * if the antenna system is badly tuned
   * if the antenna system is somehow broken or damaged
