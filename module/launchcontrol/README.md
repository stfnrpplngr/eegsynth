LaunchControl module
====================

The goal of this module is to receive input MIDI commands from a Novation LaunchControlXL. The values of the sliders and knobs are sent as control signals to the REDIS buffer. The button press and release events are sent as triggers to the REDIS buffer.


** Requirements **

The LaunchControlXL should be connected to an USB port.
The REDIS buffer should be running.