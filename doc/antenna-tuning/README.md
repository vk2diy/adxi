# Antenna Tuning

## Manual methods

Generally some sort of external box / unit is used. Within that unit is typically an analog meter showing the __forward power__ and (sometimes simultaneously) __reverse power__ levels, which are individually metered after splitting the directional elements using a device called a directional coupler. Some devices can only read one at a time, these are known as power meters.  The relationship between the forward power and reverse power is known as the __standing wave ratio (SWR)__.  Those devices which can meter both and display the ratio are known as __standing wave ratio (SWR) meters__.

Some power units / SWR units include variable capacitors and inductors which can be tweaked to obtain a better match. Other times there is a separate antenna tuning unit (ATU) which performs this function.

Many people build these by themselves with soldered components, it has apparently been a classic HAM project for many years.

The tuning process has been semi-automated by some people who generate different frequency signals and read SWR back to determine nominal 'fit-ness' of the antenna at different frequencies.

Examples of such approaches:
 * https://web.archive.org/web/20200220050317/http://www.hamstack.com/project_antenna_analyzer.html
   * Based on https://www.instructables.com/HF-Antenna-Analyser-With-Arduino-and-DDS-Module/
 * https://github.com/jmharvey1/DDS_AD9850_AntennaAnalyzer also profiled at https://hackaday.com/2015/08/06/40-antenna-analyzer-with-arduino-and-ad9850/

After making some readings, variables can be changed (ie. variable capacitors or inductors tweaked, different antenna connected, elements reconfigured in multi-element or reconfigurable antennas, etc.), until you get a better match.

This can obviously become a bit tedious if you are frequently swapping antennas or doing the "out and about" thing, which has made some people want to automate further.

## Automated methods

Some people have automated the tuning process using large backs of those horrible old clicky mechanical relays, which are just switches that turn one circuit on and off when power is applied to a different circuit.

Examples of such approaches:
 * http://www.ok2zar.cz/php/show_page.php?soubor=auto_tuner/auto_tuner.html
   * Based on http://f5rds.free.fr/F5RDS_remote_antenna_tuner.html
 * https://k6jca.blogspot.com/2016/01/antenna-auto-tuner-design-part-10-final.html (best project of the category in my view, especially the notes on [antenna tuning](https://k6jca.blogspot.com/2015/07/antenna-auto-tuner-design-part-6-notes.html) and [directional couplers](https://k6jca.blogspot.com/2015/07/antenna-auto-tuner-design-part-5.html))
 * http://www.krait-technologies.com/20240227_kt-005.pdf

However, clicky mechanical relays have a few problems.
 * They are big
 * They cost money
 * They take quite a long time to actuate
 * They take a lot of power to actuate
 * They can create a fairly large electrical impact on nearby circuits
 * They eventually wear out

## Conclusion

These days it makes more sense to use solid state alternatives wherever possible, because solid state switching is faster, more efficient, more reliable, and doesn't make noise.

While it would theoretically be possible to integrate an antenna tuning unit in to the adxi board, it seems like it would be more suitable as a later project.
