# adxi

## Timeline

 * Conceived: 2024-08-03
 * Designed: 2024-08-03 - 2024-10-10ish
 * Ordered: 2024-10-24
   * Cost: $41.40 for 10 boards + $154.20 for 10 pieces SMT = $195.60 for 10 pieces / 10 = $19.56 each (ex shipping)
   * Note that the ordering was delayed for 2 weeks or something owing to the late stage module design needing revision and wanting to share shipping costs, and this required updates to the [classe2-calculator](https://github.com/vk2diy/classe2-calculator) software.
 * ETA: 2024-11-06 
 * Received: 2024-11-04 (~midday) - total time since ordering ~10-11 days
 * Testing:
   * 2024-11-04: Blew up two boards, discovered USB power issue.
   * 2024-11-05: USB hub, audio and MCU passthru verified with bypass supply. Restored lab to functionality. Worked on a fix, ordered parts.
   * 2024-11-06: Parts received. Testing done manually powering the `TUSB321` chipset and negotiation appears to occur. This suggests a fixable situation. The boost converter still needs debugging.

## Initial test

 * Visual inspection
   * No obvious defects
   * The silkscreen now appears to be printed with an inkjet and is much less clear than previous eras
 * Multimeter inspection
   * The GND net appears to be consistent across the board
   * None of the power nets short to GND
 * Assembly test
   * Hard to get the cable through the hole.
   * While easy to thread (dimensions are fine) I failed to account for the solid plug being in the way of the cable
 * Fiddly to tighten nylon nuts around standoffs

## Initial soldering

 * Found pins for MCU not easy to solder, maybe soldermask problem
 * Put one in backwards (oops!)
   * Result: First destroyed board. Nine remain.

## Issue #1: USB-C Power Distribution
 * Next board tried connecting USB-C to a powered USB2 hub just to probe board power
 * See some power on USBC = 0.xV and USBC CLEAN = 0.xV but nothing elsewhere, have to trace back using schematic.
 * Soldered some test leads on to the related test points
 * Configured oscilloscope to view these channels:
   * The scope shows 300mV for CH2 = USBC CLEAN and 500mV for CH1 = USBC
 * Both boards show this issue, which suggests a probable design problem
 * Test results for all three cases (backwards MCU on otherwise new board, no MCU on new board, correct orientation MCU on new board):
   * Test point '5V' = 0V
   * Test point 'USBC' = 500mV
   * Test point 'USBC CLEAN' = 300mV
   * Net 'USB-C-VBUS' = 5V
 * __Conclusion__
   * Design, configuration or placement problem regarding `TUSB321` chipset.
   * Chip is too small to probe directly. but pins are as follows:
     * CC1 = bidirectional USB PD channel
     * CC2 = bidirectional USB PD channel
     * ...
   * __Hypothesis__
     * I misunderstood the datasheet.
       * Instead of the chip relaying the power, which is obtained through the CC channels, it in fact requires a separate supply, which it was not given (and I was treating as an output).
       * Therefore, no power was being relayed to the rest of the board.
       * Additionally, the last page of the datasheet specifies that a 100nF bypass should be present at the VDD pin.
     * The good news is this should be possible to fix without a board revision by bringing VDD power from the 5V verified as present on the `USB-C-VBUS` net, after the ferrite bead.

 * __Attempted fix #1: Jumper cable__
   * Soldered a cable between the `USB-C-VBUS` output after the ferrite and the `USB-C-CLEAN` net (which connects to the `TUSB321` `VDD` pin.
   * __Hypothesis__
     * This should have taken 5V to the 5V clean output as input to the `TUSB321` boost converter, allowing it to negotiate more power.
   * __Result__
     * The `TUSB321` boost converter released magic smoke instantly.
     * Second destroyed board. Eight remain.
   * __Analysis__
     * IC orientation is visually verified as correct
     * Unsure why this occurred, in particular:
       * Given that 5V was measured
       * Given `TUSB321` is supposed to have thermal shutdown
       * Given `TUSB321` only has two inputs, the feedback pin and the main input pin, the latter receiving 5V only
       * Given that the feedback circuit had been modeled.
   * __Conclusion__
     * Design, configuration or placement issue within the `TUB321` circuit
   * __Potential next steps__
     * Use the first destroyed board where this section is intact to test the circuit more carefully using a bench supply and the oscilloscope.
       * This will rely on restoring the test equipment network which appears to be down right now.
       * Very short pulses of power or power with a current cutoff could be measured on the input, output and feedback pins to understand the behaviour without destroying the chip.
       * In the worst case, it should be possible to simply relegate this portion of the circuit to next edition and power the board through the 12V test point.
       * If it appears things are generally in order, then, to reduce inrush current, bulk capacitors could perhaps be disconnected.
     * Bypass the power stage with a direct supply

 * __Attempted bypass #1: Direct 12V supply__
   * Prepared an LXI network configurable power supply Rigol DP832 to connect to 12V test point and GND test point
     * Channel configuration is 12V with overvoltage protection enabled, and 0.05A with overcurrent protection enabled
   * A timed script will enable power for a short time so that the oscilloscope can capture the effect of the power on the other power rails (5V, 3.3V) which should come up.
     * The current limit will be iteratively increased slightly until bring-up succeeds.
     * If these come up, based on the MCU module's internal regulator, then we should be in business, and can move on to testing USB functionality.
     * We may also discover additional problems, although shorts have already been ruled out with multimeter-based continuity probing.
   * Before this test can proceed:
     * I had to debug some issues with my test network due to long period of disuse (network cable had been removed and replaced for another purpose)
     * I had to verify connectivity to the oscilloscope (for screenshot capability) and power supply (for control purposes)
     * It would be good to to first verify the script and control circuit with no load using the multimeter.
   * Configuration screenshot: ![image](debugging/psu-screenshot-12vtest-preconfig.png)
   * Script output: 
```
Tue Nov  5 09:21:44 AM AEDT 2024
DP832 PSU
 - Status: OFF
 - Version: RIGOL TECHNOLOGIES,DP832,DP8C233203778,00.01.16
 - Self test: TopBoard:PASS,BottomBoard:PASS,Fan:PASS

Turning channels off... OK
Setting up channel #1
 - Voltage: 24.000V
 - Voltage limit: 24.000V
 - Voltage limiting: ON
 - Current: 0.500A
 - Current limit: 0.500A
 - Current limiting: ON
Setting up channel #2
 - Voltage: 12.000V
 - Voltage limit: 12.000V
 - Voltage limiting: ON
 - Current: 0.050A
 - Current limit: 0.050A
 - Current limiting: ON
Setting up channel #3
 - Voltage: 5.000V
 - Voltage limit: 5.000V
 - Voltage limiting: ON
 - Current: 0.500A
 - Current limiting: ON

Triggering channel 2 (12V) for test period
 - Enable
Saved screenshot_192.168.8.3_2024-11-05T09:21:44.png
 - Disable

Tue Nov  5 09:21:45 AM AEDT 2024
```

   * Analysis:
     * The screenshot showed no current consumption
     * Connections were therefore checked and an alligator clip was replaced with a soft solder tie-down to the test point
     * The script still ran without change, however re-enabling the channel manually resulted in an overcurrent alarm
     * The current was manually increased as follows: 0.1A, 0.2A
     * At 0.2A power-on occurs and the LED from the MCU can be seen, but this is not reliable.
     * At 0.3A reliability is attained ![image](debugging/psu-screenshot-12vtest-newconfig.png)

```
Tue Nov  5 09:37:42 AM AEDT 2024
DP832 PSU
 - Status: OFF
 - Version: RIGOL TECHNOLOGIES,DP832,DP8C233203778,00.01.16
 - Self test: TopBoard:PASS,BottomBoard:PASS,Fan:PASS

Turning channels off... OK
Setting up channel #1
 - Voltage: 24.000V
 - Voltage limit: 24.000V
 - Voltage limiting: ON
 - Current: 0.500A
 - Current limit: 0.500A
 - Current limiting: ON
Setting up channel #2
 - Voltage: 12.000V
 - Voltage limit: 12.000V
 - Voltage limiting: ON
 - Current: 0.300A
 - Current limit: 0.300A
 - Current limiting: ON
Setting up channel #3
 - Voltage: 5.000V
 - Voltage limit: 5.000V
 - Voltage limiting: ON
 - Current: 0.500A
 - Current limiting: ON

Triggering channel 2 (12V) for test period
 - Enable
Saved screenshot_192.168.8.3_2024-11-05T09:37:43.png
 - Disable

Tue Nov  5 09:37:44 AM AEDT 2024
```

   * Conclusion:
     * Board is at least partly functional with MCU power-on detected
     * Additional channels of 5V and 3.3V also come up as follows ![image](debugging/scope-screenshot-12vtest-powerup.png) ![image](debugging/scope-screenshot-12vtest-powerup-wider.png)

## USB testing

Now that we have power, it may be possible to test USB connectivity.

Firstly we should take care before plugging in the USB to ensure that the USB VBUS does not burn anything else. The jumper lead that allowed this to burn the boost converter has been removed and the initial state (some minor voltage seen through `TUSB321` `VDD` pin presumably bleeding through from `VBUS_DET` via the large resistor) should be replicated. Since this is insufficient to enable `TUSB321` we should see it remain idle, and the subsequent power stage which burned, namely the jumpered input to the boost converter `MT3608B`, has been removed. Subsequent diodes should prevent further issue.

So the plan is:
 * Plug in USBC
 * See whether anything burns or gets hot
 * If not, then proceed to apply power.
 * After applying power, see if the USB hub comes up, USB audio chipset comes up, or the passthru to the MCU for serial control and programming over the shared USB-C line works.

Here we go... success! `dmesg` output showed the following.

```
[131935.240875] usb 5-4.3: new high-speed USB device number 9 using xhci_hcd
[131935.354394] usb 5-4.3: New USB device found, idVendor=1a40, idProduct=0101,
bcdDevice= 1.00
[131935.354397] usb 5-4.3: New USB device strings: Mfr=0, Product=1, SerialNumbe
r=0
[131935.354399] usb 5-4.3: Product: USB2.0 HUB
[131935.364516] hub 5-4.3:1.0: USB hub found
[131935.364585] hub 5-4.3:1.0: 4 ports detected
[131935.747540] usb 5-4.3.2: new full-speed USB device number 10 using xhci_hcd
[131936.021358] usb 5-4.3.2: New USB device found, idVendor=1a86, idProduct=7523
, bcdDevice= 2.54
[131936.021362] usb 5-4.3.2: New USB device strings: Mfr=0, Product=2, SerialNum
ber=0
[131936.021365] usb 5-4.3.2: Product: USB2.0-Ser!
[131936.360870] usb 5-4.3.1: new full-speed USB device number 11 using xhci_hcd
[131936.635396] usb 5-4.3.1: New USB device found, idVendor=0d8c, idProduct=0012
, bcdDevice= 1.00
[131936.635398] usb 5-4.3.1: New USB device strings: Mfr=1, Product=2, SerialNum
ber=0
[131936.635399] usb 5-4.3.1: Product: USB Audio Device
[131936.635400] usb 5-4.3.1: Manufacturer: C-Media Electronics Inc.
[131936.675747] input: C-Media Electronics Inc. USB Audio Device as /devices/pci
0000:00/0000:00:02.1/0000:03:00.0/0000:04:0c.0/0000:14:00.0/usb5/5-4/5-4.3/5-4.3
.1/5-4.3.1:1.3/0003:0D8C:0012.0009/input/input33
[131936.734251] hid-generic 0003:0D8C:0012.0009: input,hidraw8: USB HID v1.00 De
vice [C-Media Electronics Inc. USB Audio Device] on usb-0000:14:00.0-4.3.1/input
3
[131936.762002] usbcore: registered new interface driver usbserial_generic
[131936.762010] usbserial: USB Serial support registered for generic
[131936.766921] usbcore: registered new interface driver ch341
[131936.766929] usbserial: USB Serial support registered for ch341-uart
[131936.766937] ch341 5-4.3.2:1.0: ch341-uart converter detected
[131936.767494] ch341-uart ttyUSB0: break control not supported, using simulated
 break
[131936.767523] usb 5-4.3.2: ch341-uart converter now attached to ttyUSB0
[131937.067790] usb 5-4.3: USB disconnect, device number 9
[131937.067792] usb 5-4.3.1: USB disconnect, device number 11
[131937.137341] usb 5-4.3.2: USB disconnect, device number 10
[131937.137450] ch341-uart ttyUSB0: ch341-uart converter now disconnected from t
tyUSB0
[131937.137464] ch341 5-4.3.2:1.0: device disconnected
```

This tells us that:
 * USB data lines work both on the host-side and the board-side
 * The USB hub works
 * The audio chipset is detected
 * The USB cable passthru to the MCU module works
   * The CH341 serial UART on the MCU is detected

Fantastic! Let's power it on a bit longer to get a USB tree display.

```
        |__ Port 003: Dev 015, If 0, Class=Hub, Driver=hub/4p, 480M
            |__ Port 001: Dev 017, If 0, Class=Audio, Driver=snd-usb-audio, 12M
            |__ Port 001: Dev 017, If 1, Class=Audio, Driver=snd-usb-audio, 12M
            |__ Port 001: Dev 017, If 2, Class=Audio, Driver=snd-usb-audio, 12M
            |__ Port 001: Dev 017, If 3, Class=Human Interface Device, Driver=usbhid, 12M
            |__ Port 002: Dev 016, If 0, Class=Vendor Specific Class, Driver=ch341, 12M
```

Great. 

Here we can see four device interfaces on the audio chipset, three audio and one USB HID (used for microphone buttons).

The audio devices are used to receive audio from and send audio to the transceiver.

The final device is the MCU module's CH341 serial UART interface which is used for serial control and programming.

## Next steps

A reasonable step might now be to __attempt to program the device__ in order to better verify on-board functionality.

Alternatively, we could __go back and try to solve the USB C power distribution issue__.  Let's do that as it's annoying me that we've been so lucky with the later-stage USB devices but failed with the base power.

## Back to the USB power distribution problem

It seems that what may have happened is that I misunderstood the USB-C power distribution system, as it is my first time designing both USB devices and USBC powered devices.

Basically, there are three logical lines related to power on the USB C standard:
 * The `VBUS` line, which is the USB bus voltage. This goes all the way back to USB 1.0.
 * The `CC1` and `CC2` lines, which are new to USB-C and used for the negotiation of more power.

It seems that my wrong-headed design-time assumption was that the power would be negotiated on *and distributed on* the `CC1` and `CC2` lines, because `VBUS` has far too many backwards compatibility issues to be brought up to a high voltage and amperage.

However, it seems this assumption was wrong, and that in fact the `VBUS` line is used for the power distribution and the `CC1` and `CC2` lines are only used for power negotiation. This is odd to me, but I suppose that's how it is, because it would explain our situation as follows:
 * The `TUSB321` chip never comes up
 * The `TUSB321` documentation final page suggests adding a 100nF bypass cap on the `VDD` pin (implying external power input required through this pin)
 * The direct connection between `VBUS` and the boost converter fried it, because:
   * After `VDD` was powered on for `TUSB321` (since it's on the same net that was directly powered), it negotiated more power which was in excess of the boost converter `MT3608B` `IN` pin's absolute maximum voltage.

This is a sketchy comprehension but seems like it may be heading in the right direction.

If that holds, and we could probably do some further testing to verify the theory, then:
 * In terms of safely bringing up the TUSB321 using only USB power, we could perhaps cut the connection from VDD to the `MT3608B` and instead connect it to pin 5 (`VBUS_DET`) which lies behind a protective 909K resistor which the `TUSB321` datasheet states is for reducing modern high VBUS voltages to a safe small level. Presumably this power level may be adequate for powering the chip.
 * The `TUSB321` datasheet says that it should be functional at 4.5V, that all pins have an absolute maximum of 6-6.3V, and that the threshold voltage should be 4V
 * We should perhaps go back to re-measure the threshold voltage presented before and after the 909K resistor, however I believe the voltage is well below 1V and thus insufficient.

Some potential fixes:
 * Some __parallel, alternate resistor configuration__ to obtain a higher voltage (eg. 200K instead of 909K)
 * A __5V regulator__ capable of the higher voltages that may be presented on the `VBUS` line
   * Most regulators seem to fail around 17V (AMS1117)
   * I found a local supply of 35V 1.5A capable 5V regulators, L7805CV, and procured them. They should arrive tomorrow.
 * A __12V regulator__ to reduce the `VBUS` line (if higher than 5V) down to 12V stable, instead of the current boost converter

![image](debugging/possible-power-fix.png)

## The Plan

 * Cut the connection between the `TUSB321` and the `MT3608B`.
 * Wire a 5V regulator output or a resistor setup to the `TUSB321` chip's `VDD` pin.
 * Instrument `CC1`, `CC2`, `VDD` and the USB `VBUS` line.
 * Run a power-up test capturing oscilloscope output to verify that `TUSB321` is now powering up correctly, and what effect this has if any on the `VBUS` line voltage.
 * Then, move on to `MT3608B` subsystem testing based on the newly clarified and verified context.
   * If, as suspected, the `TUSB321` negotiates changes to the `VBUS` line that present a voltage higher than desired for the `MT3608B`, use a 12V regulator module instead.
   * If, after verifying power-up, the `TUSB321` negotiates changes to the `VBUS` line that only present a higher amperage, further consideration will be required.

## Regulator insertion

It seems this test point is the correct place to target: solderable, large, out of the way.

![image](debugging/5v-target.webp)

However, before executing that plan it may be beneficial to first use the bench supply with a low current set just to see what happens when voltage is applied.

### Bench supply pre-test

The first step was removing the `MT3608B` boost converter which had anyway blown up. After failing with the soldering iron I succeeded with the hot air gun, while holding the part with tweezers and applying horizontal pressure to dislodge it. This effectively isolates the `VDD` pin of the `TUSB321` so that the 'USBC CLEAN' test point can be used to feed it a specific and precise current from the bench supply.

The next step was to move the alligator clip for supply from the previous 12V configuration used for board bringup to 5V terminals on the PSU and this new target test point on the board.

The next step was to solder on test leads to allow instrumenting the lines of interest in order to monitor the power-up and functioning of the `TUSB321` chip.
 * `CC1`
 * `CC2`
 * `VBUS-DET` (detection pin input, after 909K resistor, at 'USBC' test point)
 * `VBUS` (post ferrite, pre-resistor)

The final step is to write a test program to set the PSU configuration and enable power temporarily.

The expected functionality is something like:
 * USB is connected to an external powered hub
 * Power is introduced to the `VDD` pin from the bench supply
 * Some sort of process occurs on `CC1` and `CC2` representing negotiation for more power
 * Change occurs on the `VBUS` and should be measured
 * The bench supply powers off

The orignal state, with USB disconnected and no power applied, is as follows.

![image](debugging/benchtest-prestate-nousb.png)

In other words, everything is at zero as expected.

More interestingly, the original state, with USB connected and no bench power applied, is as follows.

![image](debugging/benchtest-prestate-usb.png)

Here you can see:
 * `CH1` = `CC1` is ~0V
 * `CH2` = `CC2` is ~0.9V
 * `CH3` = `VBUS-DET` is ~0.5V
 * `CH4` = `VBUS` is ~5.25V

We now need to define a trigger from which to action our oscilloscope capture.

Perhaps a voltage higher than 5.5V occuring on `VBUS` would be good signal, or a signal appearing on `CC1`. Let's try the latter first, since it should occur before any VBUS rise.

I tested the proposed trigger on plugging in the USB cable and obtained this capture.

![image](debugging/benchtest-prestate-plugevent.png)

Here you can see:
 * `CH1` = `CC1` begins at an initial 0.4V or so before rapidly dropping to 0V.
 * `CH2` = `CC2` rises from an initial 0.6V to 0.9V within around 100us.
 * `CH3` = `VBUS-DET` remains stable at 0.5V
 * `CH4` = `VBUS` remains stable at ~5.25V

This may be useful as a point of comparison for subsequent captures.

Let's try powering up the `TUSB321` chipset with the bench supply and seeing what happens.

```
DP832 PSU
 - Status: OFF
 - Version: RIGOL TECHNOLOGIES,DP832,DP8C233203778,00.01.16
 - Self test: TopBoard:PASS,BottomBoard:PASS,Fan:PASS

Turning channels off... OK
Setting up channel #1
 - Voltage: 24.000V
 - Voltage limit: 24.000V
 - Voltage limiting: ON
 - Current: 0.500A
 - Current limit: 0.500A
 - Current limiting: ON
Setting up channel #2
 - Voltage: 12.000V
 - Voltage limit: 12.000V
 - Voltage limiting: ON
 - Current: 0.300A
 - Current limit: 0.300A
 - Current limiting: ON
Setting up channel #3
 - Voltage: 5.000V
 - Voltage limit: 5.000V
 - Voltage limiting: ON
 - Current: 0.100A
 - Current limit: 0.100A
 - Current limiting: ON

Triggering channel 3 (5V) for test period
 - Enable
Saved screenshot_192.168.8.3_2024-11-06T11:43:32.png
 - Disable
```

I repeated the test a few times, but in each case the screenshot showed no power draw, the scope did not trigger.

After that, attempting to power on the 5V channel manually resulted in an error about overvoltage protection.

![image](debugging/psu-screenshot-5v-overvoltage.png)

The overvoltage protection was adjusted to 5.5V and then the test was retried.

![image](debugging/psu-screenshot-5v-draw.png)

This appears to work.

However, still the scope does not trigger.

Rather than worrying about triggering, I switched it to auto mode to see if anything was visibly changing when the `TUSB321` chip is powered by the bench supply.

It was then apparent that things were changing.

Recall the USB connected, `TUSB321` unpowered state.

![image](debugging/benchtest-prestate-usb.png)

 * `CH1` = `CC1` is ~0V
 * `CH2` = `CC2` is ~0.9V
 * `CH3` = `VBUS-DET` is ~0.5V
 * `CH4` = `VBUS` is ~5.25V

Contrast the USB connected, `TUSB321` powered state.

![image](debugging/benchtest-poststate-usb-scopeshot.png)

 * `CH1` = `CC1` is ~0V (same)
 * `CH2` = `CC2` is ~0.4V (reduced from ~0.9V)
 * `CH3` = `VBUS-DET` is ~0.5V (same)
 * `CH4` = `VBUS` is ~5.25V (same)

![image](debugging/benchtest-poststate-usb-psushot.png)

We also note some 56mA of power draw evidenced on the PSU.

So what's going on here? According to the `TUSB321` datasheet, there are various signalling levels used on the `CC1` and `CC2` channels.

 * "LOW" is 0.4V, which is perhaps what we are seeing in the second state
 * "MEDIUM" is 0.28-0.56 x VDD which works out to 1.47-2.94V, most likely in the middle, or around 2.2V
 * "HIGH" is VDD-0.3V which works out to 4.95V

None of these levels appear to describe the rest state we are seeing (0.9V).

Probably it would be best not to try to spend time understanding all of the signalling state transitions and just get the thing working.

Given that the `VBUS` voltage doesn't change in this case, but some negotiation does appear to have occurred, perhaps a higher amperage 5V supply has been negotiated successfully.

Checking the power supply design notes I did state that 5V 1.5A = 7.5W was the negotiation target, so this would appear to be the case.

In terms of next steps:
 * We could connect a DC load to test what the power draw is under each scenario: no `TUSB321` power, and `TUSB321` powered and negotiations complete.
   * The hypothesis would be that ~1.5A can be drawn in the second case only.
 * Since the USB powered device which we plugged in to in this case is a USB2.0 hub, perhaps we will see a different result if we plug in to a USBC "wall wart" AC charger with known high current capability. Unfortunately that's hard to achieve in the current position due to cable length constraints and AC outlet locations on my bench.
   * While I could muck around with existing extension cords, it's a lot of hassle. Instead, I have ordered a small benchtop AC extension lead and sockets to resolve this, it should arrive tomorrow and make this feasible.
 * We could instrument the output pins of the `TUSB321` and look for state changes.

## Complete issues list

 * Cable passthru too difficult, hole should be enlarged
 * USB PD incorrect topology
 * USB PD chip missing 100nF cap at VDD
 * Boost converter self-destructs
