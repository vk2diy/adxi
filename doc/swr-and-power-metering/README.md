# SWR Monitor and Power Metering

One of the main ways that amateur radio operators traditionally evaluate their antenna system is by measuring the __standing wave ratio (SWR)__ of the antenna system.

The __SWR__ is simply the ratio of power forward (being sent out) to reverse (being reflected back), ie:

SWR = P<sub>forward</sub> ÷ P<sub>reverse</sub>

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
   * Feed the resulting signal to the microtroller unit (MCU) ("brain") on a pin with an analog to digital converter (ADC) in order to sample the level

This should allow us to basically obtain power levels for each direction, and to simply compute the SWR.
