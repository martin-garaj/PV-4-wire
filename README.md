# Project 

This is an ad-hoc solution for replacing high-precision 4-wire measurement setup by multiple simple instruments orchestrated by PC running a Python script.

There might not be any use for this anymore, but since the interfaces for the devices change by glacial pace, the scripts and control mechanism are and will be relevant for several more years, maybe decades.

Also, not to toot my own flute, but replacing a high-precision machine worth 100k ~ 200k Euro by a set of (relatively) cheap instruments that match the precision and extend the measurement range, is an **achievemnt** for me. Not to mention, that this was done hastily, since the original machine broke unexpectadly during my short-term exchange during my PhD.


# Measurement setup

The image below shows the connections of the components.

Refer to /docs/Publication_3__hardwareX.pdf for more information.

![measurement-setup](/images/setup.png "Illustration of interconnected components of the 4-wire measurement setup.")


# Measurement range

The 4-wire setup is meant to measure 3 quadrants of PV panle operation. PV panle, a semiconductor device working as a generator or load (depending on operating point), has exponential characteristic, both in generative mode and in reverse-bias mode. This is both challenging to measure and interesting to study (for renewable energy enthusiasts).

![measurement-range](/images/meas_range.png "Measurement range of the 4-wire measurement setup (green & yellow) over-layed by PV panel characteristic (black line) on top of measurement range of Keithley 2651A (blue).")


# How to

Study the code (especially for National Instrument measurement card) and use it in your own projects. Make sure you have proper grounding and understand the measurement ranges of your sensors.
