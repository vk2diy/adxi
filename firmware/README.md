# Firmware directory

Firmware may be compiled using [platformio](https://piolabs.com/), which provides a vendor-neutral command line environment for embedded development supporting modern features such as continous integration, unit testing and operating system independence.

## Installing platformio

See [What is PlatformIO?](https://docs.platformio.org/en/latest/what-is-platformio.html?utm_source=github&utm_medium=core) and then either [PlatformIO IDE](https://docs.platformio.org/en/latest/integration/ide/pioide.html) or [PlatformIO CLI](https://docs.platformio.org/en/latest/core/index.html).

## Using platformio

### Python venv

You may need a python virtual environment to run. This cross-platform mechanism provides a way for different python environments to be manage on one system.

In order to create a python virtual environment, run `python venv init`.

In order to enter a pre-existing python virtual environment, change to the correct directory at the top of the tree and run `. ./bin/activate`.

In this environment, all python commands (including `pio` for platform IO) will use the virtual python environment and its packages.

When you are done, type `exit` to return to the normal system shell.

### General use

To compile simply type `pio run`.

For other commands, see [CLI command list](https://docs.platformio.org/en/latest/core/userguide/index.html#piocore-userguide).

For example:

 * `pio project config --lint` will verify project configuration.
 * `pio package install` will install missing dependencies.
 * `pio pkg update` will update dependencies.
 * `pio check` will run a static code analysis.
 * `pio run` will build the project.
 * `pio run -t upload` will upload the project to the device.
 * `pio test -h` will show testing related commands.

## Firmware architecture

Similar to other Arduino-inspired firmware, the general architecture of the firmware is as follows.

 * The firmware sets up the various pins of the microcontroller in its `setup()` routine.
 * The firmware then iterates repeatedly through a `loop()` routine.

The loop routine varies in its function depending upon operating mode and input, for example:
 * It may receive and send information from and to the host computer via USB serial interface.
   * The physical chip in use for serial UART interface on most Arduino Nano MCU modules is the CH341. In the past this needed drivers for various systems and did not work well on many Macs. It works well on Linux. If you are using Windows or similar, you may need to find a driver.
   * The protocol used for this purpose is an emulated subset of the Kenwood TS-2000 protocol, as [implemented](https://github.com/Hamlib/Hamlib/blob/master/rigs/kenwood/ts2000.c) in the [hamlib](https://github.com/Hamlib/Hamlib/) library which drives the [WSJT](https://wsjt.sourceforge.io/) software. The protocol is documented on pages 114-141 of the [Kenwood TW-2000 owner manual](https://erikarn.github.io/kenwood/TS-2000/TS-2000-Owner-Manual.PDF) ([wayback machine archive](https://web.archive.org/web/20240713202306/https://erikarn.github.io/kenwood/TS-2000/TS-2000-Owner-Manual.PDF), [archive.today archive](https://archive.is/gLoBM)).
   * It may reconfigure, enable or disable the radio and audio subsystems for disparate frequencies and output power levels.
   * It may obtain forward power or reverse power readings.
   * It may calculate standing wave ratio (SWR) readings from forward and reverse power readings.

