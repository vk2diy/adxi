# USB Audio Chipset

## Requirement

The original ADX project required audio lines to and from the computer, a programming cable, and an additional power cable.

This was a total of four cables.

Given that it was easier to add USB power distribution (USB-PD) support to the [power supply](../power-supply) module than add batteries and a battery management system, the decision was made to progress with adding a [USB hub](../usb-hub/) at which point adding a USB audio chipset seemed the logical next step.

By adding an additional USB port for plugging in the MCU module, we can provide access to all system components over one cable.

## Available chipsets

A cursory review of available chipsets concluded that the CMedia CM108B was the cheapest component that was available for surface mounting which would provide the required functionality.

## CM108B configuration

The chip has various capabilities in terms of connectivity including [SPDIF](https://en.wikipedia.org/wiki/SPDIF) and [I2S](https://en.wikipedia.org/wiki/I%C2%B2S) which we do not require. The only features we require are analog microphone input and analog audio output.

In addition, EEPROM support, volume management, HID button host integration, mute functions, AA path (analog mixing) and other options are largely superfluous to the application requirement and are ignored.
