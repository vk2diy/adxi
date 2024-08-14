# adxi - ADX Improved

ADX is abbreviation for Arduino Digital Xceiver, a project emphasizing simplicity and Arduino hardware creating a [direct-conversion receiver](https://en.wikipedia.org/wiki/Direct-conversion_receiver) focused on [digital modes](http://www.arrl.org/digital-data-modes).

This fork is called __adxi__ (or "ADX Improved") with the following changes:
 * __restores access to the project for modern KiCad__
 * __integrates known bug fixes__
 * __full computer control__ (remove buttons/blinkenlights interface)
 * __broader power supply acceptance__ (~12-36V nominal)
 * __improved filtering__
 * __supports more amateur bands__: 70cm/2m/10m/15m/17m/20m/30m/40m/60m/80m/160m/630m/2200m - only missing 23cm
 * __use of modern surface mount components__ for repeatability
 * __improved documentation__ hoping to facilitate learning
 * __using platformio__ to manage the firmware build and dependencies in a modern way

## Update (2024-09-11)

 * [Further work on power amplifier theory and component selection](doc/class-e-pa/)

## Updated (2024-09-13)

Recent work:
 * More work on power amplifier
   * Three-mode RF choke inductor mostly completed (one tier to be re-specified)
   * Switchable capacitance calculated and to be added
 * Input of general dimensions of two boxes which have been selected as possible form factors. Have another idea to use this sort of thing as a modular approach: ![image](tiffin.webp)
 * General cleanup of schematic

## Updated draft PCB (2024-09-10)

![image](adxi-draft-pcb-2024-08-10.webp)

 * Further consideration of overall layout, switching placement.
 * It seems there will need to be a series-parallel array of RF choke inductors to cover the broad target frequency range.
   * This is not necessarily expensive, just complex.
   * There will also be at least one switchable inductor in the main RF choke.
 * Other additions:
   * I2C LCD pin header
   * Further antenna connector (MMCX)

## Updated draft PCB (2024-09-09)

![image](adxi-draft-pcb-2024-08-09.webp)
![image](adxi-draft-pcb-2024-08-09-rear.webp)

This version adopts a band-module approach in order to reduce iteration cost.

The basic notion is that a 7x3cm module can be plugged in to provide band-specific low pass filtering.

There is space on the front of the PCB for three of these modules, and on the rear of the board another three modules. Modules are staggered to minimize the effects of electromagnetic coupling between modules and their terminals. Sockets are used on the board and pins on the filter modules in order to reduce the volume of metal present when less filters are connected.

## Initial draft PCB (2024-08-07)

![image](adxi-draft-pcb-2024-08-07.webp)

 * Draft now changed, potentially to have pluggable LPFs instead of a monolithic all-band-onboard architecture
   * This requires the design of an interface for the same
 * Filter switching added

## Current documentation
 * Filters
   * [Bandpass filter model](doc/filter-models/bandpass-filter/) showing audio frequency bandpass filter
   * [CD2003 5V supply filter model](doc/filter-models/cd2003-supply-low-pass-filter/) showing power supply filtering for the radio receiver chipset
   * [DC blocking filter](doc/filter-models/dc-blocking-filter/) showing how capacitors block DC and their nominal frequency relationship
 * Schematic design notes
   * [Multi-band low pass filters](doc/multi-band-lpfs) showing various third party designs for multi-band LPFs and including notes considering practical aspects of the design problem.
   * [SWR and power metering](doc/swr-and-power-metering) discussing the planned approach to obtaining this information simply
 * Wireless protocols
   * *[The FT4 and FT8 Communication Protocols](doc/wireless-protocols/FT4_FT8_QEX.pdf)*

## ADX Original Project

### Features

 * ADX is a mono band (actually quad band) digital modes optimized HF transceiver that can cover four pre-programmed bands one band at a time by swapping Band LPF Modules.
   * It can work on 80m, 40m, 30m, 20m, 17m, 15m and 10m bands
   * It can operate on four of the most popular digital modes, FT8, FT4, JS8call and WSPR.
 * ADX supports computer control (CAT) by emulating KENWOOD TS2000 HF Transceiver over a 9600 8N1 serial link to control Band and Mode changes.

### Goals

The project was originally designed by [Barb (WB2CBA)](https://github.com/WB2CBA/ADX) ([original project website](https://antrak.org.tr/blog/adx-arduino-digital-transceiver/))  with the goal to design a simple HF Transceiver optimized for operating on Digital modes:
 - Simple to procure – meaning not effected by chip shortage
 - Simple to build – 2 modules, 2 IC’s and 4 Mosfets!
 - Simple to setup and tune – One simple calibration procedure is all needed.
 - Simple to operate – Plug in ADX MIC to soundcard MIC input and ADX SPK to PC soundcard speaker input and we are good to go with any digital modes Software.
 - Dirt Cheap – Costs less than 25$ to get all parts and PCB if we exclude ridiculous shipping costs!
 - Plug in a USB cable between ADX Arduino and your PC, Select Kenwood TS2000 with 9600bps,8,1 setup as your CAT rig and you will have CAT control on ADX!

It has since been built all over the world.

### Design

The original design was based on the following major physical modules:
 * Main ADX PCB
   * CD2003 radio chip
   * 74ACT244 buffer/line driver
 * Arduino Nano (ATmega328P MCU module)
 * Si535x clock generator module
 * uSDX LPF band module
 * External PC microphone interface (for sending received signals to the computer)
 * External PC speaker interface (for receiving encoded signals from the computer)

## Revised design

The revised design is not religiously focused on minimizing the number of components through using external circuit boards.

Instead, it:
 * brings the clock generator and band-specific filters on-board
 * seeks to remove the physical interface and replace it fully with host computer control (known as a "computer aided transceiver" or "CAT") via [wsjtx](https://wsjt.sourceforge.io/) (G4WJS/K9AN/IV3NWV) which is itself based on [hamlib](https://hamlib.github.io/) (VK3FCS/F8CFE/etc.)
 * provides a more flexible and well filtered power supply so that available AC-DC ~12-36V inputs can be used

## Building the firmware

Firmware is managed through [platformio](https://github.com/platformio/platformio-core).

Rationale:
 - While excellent in its simplicity, Arduino IDE is generally inappropriate for long lived projects.
   - Why?
     - It has brittle dependency management
     - It relies on non-scriptable GUI actions.
     - It lacks modern features like unit testing, CI/CD, etc.

Result:
 - You will need to install either [platformio-core](https://github.com/platformio/platformio-core) (command line) or [platformio IDE](https://platformio.org/platformio-ide).

Benefits:
 - Notes about specific versions of specific libraries and compatibility are now a thing of the past.
 - The addition of future libraries, compilers, or tools is easy
 - Users become familiar with more modern, cross platform and professional grade approach to firmware development and management while working on personal projects

### Under platform-io core (command line)

Simply change to the source code directory and type `pio run`.

```
$ cd firmware
$ pio run
```

### Under platformio IDE

Open the project in the IDE then use the buttons provided.


## Current status of this fork

 - Firmware now builds correctly under platformio
 - KiCad 8 redrawing of the schematic and a draft layout are well underway and nearing completion

### Next steps
 - Complete schematic and layout
 - Order boards
 - Verify functionality

## History

### 2024-08-07
 - First 'mostly there' release of Kicad v8 schematic and board design

### 2024-08-03

 - Forked, general cleanup and migrated to [platformio](https://github.com/platformio/platformio-core).
   - Previously Arduino IDE builds were the norm
   - Apparently the files had apparently not been opened since KiCad v4 ... KiCad is now at v8.0.4
 - Outstanding issues
   - KiCad has altered its library management so much that the old files will not import directly to v8.0.4
   - KiCad has improved its internal libraries so that external libraries for many parts are no longer required
   - KiCad has integrated the historic DigiKey library
   - The schematic is missing known PCB fixes not integrated but documented by the original author
   - The schematic uses a non-standard symbol for the MCU which is unhelpful
   - The schematic has a number of further errors making it suboptimal for introducing new students
   - The layout used a type of fill which is no longer supported by modern KiCad
   - The layout can probably be improved
 - Conclusion
   - Given the simple nature of the schematic it is better at this point to redraw the schematic and redo the layout, removing all previous KiCad 4 era files

### 2023-07-14

- Release band display bug fixes by Peter Petrov (LA7WRA) and Mark Culross (KD5RXT).

### 2023-06-10

- Cowtown Amateur Radio Club ADX Buildathon Construction Manual v1.5 by Richard Hinsley (W5ARH/VK2ARH)

### 2023-04-08

- SI5351 module pull up resistor fix added to build manual v1.4 by Richard Hinsley (W5ARH/VK2ARH)

### 2022-12-20

- Calibration procedure changed to protect EEPROM from R/W wear.
- Add zener diode PA mosfet protection from excessive SWR conditions.

## Contributors

### adxi project

 * VK2DIY

### ADX Project

 * [Barb (WB2CBA)](https://github.com/WB2CBA/ADX): Project conception and original design.
 * [Richard Hinsley (W5ARH/VK2ARH)](https://www.qrz.com/db/W5ARH): Buildathons, outreach and build documentation.
 * [Joerg Frede (DK3JF)](https://www.qrz.com/db/DK3JF): CAT and other software contributions.
 * [Peter Petrov (LA7WRA)](https://www.qrz.com/db/LA7WRA) and [Mark Culross (KD5RXT)](https://www.qrz.com/db/KD5RXT): Band display bug corrections.
 * [Burkhard Kainka (DK7JD)](http://elektronik-labor.de/): Initial FSK TX signal generation code - http://elektronik-labor.de/HF/SDRtxFSK2.html
 * [Jason Mildrum (NT7S)](https://www.qrz.com/db/NT7S): SI5351 Library - https://github.com/etherkit/Si5351Arduino
 * [Lajos Höss (HA8HL)](https://www.qrz.com/db/HA8HL): Inspiration for CAT code based on his TS2000 CAT implementation.
 * [JE1RAV](https://www.qrz.com/db/JE1RAV): Improved FSK TX signal generation code - https://github.com/je1rav/QP-7C
