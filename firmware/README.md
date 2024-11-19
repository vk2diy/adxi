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
