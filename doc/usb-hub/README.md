# USB Hub

The cheapest USB hub chip seemed to be `SL2.1s`.

Although [the datasheet was in Chinese](https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2106070334_CoreChips-SL2-1s_C2684433.pdf) and did not have good explanations it was understandable.

Basically the standard across vendors for USB 2.0 data pin naming appears to be `...P` for `+` or positive signal, and `...M` for `-` or minus signal.

So pins like `UDM` and `UDP` are a set, reflecting the negative and positive sides of the pair, respectively.

There are four pairs (`DMx`/`DPx`) numbered `1` through `4`, plus an unusually named pair `UDM`/`UDP` which is taken to be the uplink pair to the host computer. The `XIN`/`XOUT` are for a timing crystal, `VDDx` are power supplies, and `CSS` is ground.

For a timing crystal the required value of 12MHz is exceptionally common and thus easy to find. Some have two pins and others have found. However, for optimum operation, it is necessary to add external load capaitors. These can be calculated based upon the `CL` value of the crystal from its datasheet, plus a `CStray` value of the layout which is generally assumed rather than calculated or measured. The result using [this calculator](https://kobee.com.au/blogs/calculators/crystal-capacitor-value-calculator) was around 33pF, a common value for capacitance that is easily sourced.

A resistor based voltage divider provides 1.8V supply from the 3.3V supply.

Decoupling capacitors are provided for the 5V, 3.3V and 1.8V supply lines.
