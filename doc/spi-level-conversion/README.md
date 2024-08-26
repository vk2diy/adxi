# SPI Level Conversion

## Requirement

Because the ICs we use to drive these signals (`74HC595`) are happy to operate at 3.3V but require that input voltages are less than or equal to their supplied operating voltage, we need to convert the inbound SPI signals to 3.3V before presenting them.

## Potential approaches

There are different ways to drop the voltage output from the MCU (5V) to the 3.3V required for communicating with the modern ICs on the board.

These methods vary mainly in terms of directionality (unidirectional or bidirectional), reaction time / signal speed suitability, protection level, cost and layout overhead.

The simplest method, which is only unidirectional and additionally has issues with high speed signals, is suitable for this situation and is simply a voltage divider.

Using only three 1K resistors, we can achieve the level conversion without additional hassle or introducing new components.

This is a highly cost effective method of achieving the required level conversion which comes at the cost of some board space.

## Component selection

While we could use very small resistors (0402, etc.) the choice was made to keep these components at 0603 sizes since it is felt that the external exposure represented by USB bus voltages (unknown outside devices, connection event discharges, etc.) might sometimes include transients and it is felt that 0603 components are substantially less brittle than 0402s in terms of their transient handling capacity. In general, all other things being equal, the larger the component, the greater the resistance to transients.
