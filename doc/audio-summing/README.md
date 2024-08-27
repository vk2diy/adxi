# Audio Summing

Two stereo lines need conversion to mono.

What's the best way to do this?

According to [this theory page](https://web.archive.org/web/20120509070136/https://www.rane.com/note109.html) (which itself will make a lot more sense after reading [all about audio jacks and their schematic representation](https://www.cuidevices.com/blog/understanding-audio-jack-switches-and-schematics)), the use of resistors for summing stereo to mono is probably a perfectly fine and appropriate choice unless we are audiophiles.

In such a circuit, resistors actually provide the benefit of having frequency-independent response, unlike transformers.

Upon discovering no specific information on precise resistor sizing methods for this type of application, we will seek implement the recommended circuit using 1K resistors (as sources vary from 475 ohm through 10k ohm).

In such a configuration, the differential impedance is 2K while the common mode impedance (source impedance to the output) is 0.5K.
