# Power Supply

## Requirement

ADXI aims to support 5 watt output since this is the most common output level limitation in regulations globally affecting amateur radio operators.

Given the 5 watt output goal, the majority of power consumption is going to be in trasmit power, since the rest of the components are unlikely to consume a significant amount of power.

Therefore, we should expect rapidly changing power draw as transmit is enabled and disabled, and this will nominally peak at 5 watts.

Almost all of this power will be on the 12V power supply (noting that power supply lines are conventionally termed "rail", so "12V rail" would refer to the 12V supply line).

Although the power amplifier (PA) operates at a nominal 12V, the minor current requirements for the rest of the system are mostly measured in 5V or 3.3V.

## Design evolution

Initially the design was to be made using a conventional DC input jack (as seen on the "wall wart" style power-pack supplies ubiquitous in pre USB-C electronics), however it was later reasoned that introducing USB-C would probably be feasible, and this would simplify cabling substantially from the four-cable original ADX design (DC power + USB to MCU + audio in + audio out) to a single cable design (USB-C only). The decision was made to keep both a conventional DC input jack and USB-C support to support debugging, future expansion, and flexibility.

## Design overview

There are two input power paths:

 - USB-C input power path
 - DC input jack power path

These are followed by a common power path.

### USB-C Input Power Path

The USB-C input path is governed by the TUSB321 chipset, which:
 - Detects connectivity using its `VBUS_DET` pin
 - Reads the requested USB power configuration from its `CURRENT_MODE` pin
 - Negotiates the delivery of power through its `CC1` and `CC2` pins
 - Reports on its current states through the `OUT1`, `OUT2` and `VCONN_FAULT` pins
 - Provides power through its `VDD` pin

The chip can be configured to support a range of [USB-PD (USB power delivery)](https://en.wikipedia.org/wiki/USB_hardware#USB_Power_Delivery) modes.

The mode for which the TUSB321 chipset is configured in this schematic is to request 5V 1.5A, which equates to 7.5 watts. This should provide a comfortable conversion loss margin for subsequent power stages. Modern USB-C can go much higher, but it is better not to over-specify the requirements because fallbacks and failure handling then become a requirement.

The `VBUS_DET` pin is adjacent to a resistor which provides for safe connection of the pin to the bus when the bus is in higher voltage modes. There is an additional resistor provided around 900K value in order to reduce the maximum potential bus voltage to a safe level for the IC.

The requested 5V power is however of an insufficient voltage for much of the radio circuit. Therefore, we need to upconvert ("boost") the voltage from 5V to 12V.

The inexpensive component selected for this purpose is the `MT3608B` boost converter which can be configured through a resistor divider to boost input voltages as low as 2.5V to output voltages as high as 24V and has 4A current support and relatively high and stable efficiency of around 93% declining to 90% at 1A.

The `MT3608B`:
 - Accepts an on/off control signal on its enable (`EN`) pin
 - Draws input power on its `IN` pin
 - Controls current flow with its `SW` pin
 - Determines current output state with its feedback `FB` pin

The output voltage is configured through a resistor divider ratio which is calculated as follows:
 - Desired VOUT = 12V
 - Feedback voltage from `MT3608B` datasheet = 0.6V
 - Required reistor-divider ratio = 20/0.6 = 19

We use 5.1K and 100K resistors for this purpose, as they are commonly available values matching this ratio.

An additional couple of capitors are provided to smooth the output of the boost converter before a diode which guarantees the correct direction of current flow with respect to the second potential input power path.

However, we should take note of the switching frequency which is variously described as 900kHz-1.2GHz. Therefore a model has been made showing its relationship to amateur radio bands.

![image](switching-harmonics.png)

### DC input jack power path

The DC input jack accepts external DC power from a wall-wart style power pack. It is designed to accept as broad a range of supply voltages as possible, from 12V to 36V or so.

Many people have a large number of power packs lying around within this range.

The most common physical size for this general range of voltage (and indeed the most common in general) is 5.5mm (outer diameter) and 2.1mm (inner diameter). The inner pin is the positive supply rail, and the outer sheath is the ground.

A large range of DC input jacks are available for PCB mounting, and within the same outer and inner diameter dimensions substantial variation can still be found, for example in terms of the metallurgy of the connection surfaces, the physical strength and design of the connector, the presence of one or more mounting pins designed to translate physical stresses from insertion and bending (for example due to horizontal force on the plug after it has been inserted) without stressing the relatively delicate soldered pin connections, provide different insertion angles such as perpendicular to the circuitboard, provide an insert detection signal, provide support and fallbacks for supporting less common plugs carrying multiple signals, etc.

Because we don't know what the user will plug in here, we have to treat it as suspect.

The first stage is a ferrite bead for high frequency filtering.

The second stage is clamping to 24V to ensure subsequent components are exposed to a tolerable voltage range.

A diode then ensures this input path behaves correctly after combination with the alternate USB-C input path.

### Common power path

Subsequent to the individual input power paths, a common path occurs.

This consists of bulk capacitance to provide a stable basis for subsequent power. Here we parallel two 470uF electrolytic capacitors to provide a lower [equivalent series resistance](https://en.wikipedia.org/wiki/Equivalent_series_resistance) and some increased longevity in the face of potential capacitor decay, as well as provide filtering.

The filtering is broken in to two parts, a capacitor filter using 100nF and 10nF capacitors which are suitable for high frequency attenuation, and an inductor.

The resulting net is termed `VIN` and is used as input to the regulator, an `L7812`, which provides the final 12V rail to the system.

For the 5V and 3.3V supplies, we rely on the onboard regulator on the MCU module.