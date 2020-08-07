# pi-radio
Control mpd playlists using hardware buttons on Raspberry Pi.

# Setup

## MPD

You will need to setup an mpd server on your raspberry pi. Alternatively, you can edit the script to point it at an existing server. 

## Hardware

The project was developed using a Raspberry Pi 3B+ but will work on most (if not all) models. The button connections to the GPIO pins are as follows:

- Play/Pause - 22
- Volume up - 17
- Volume down - 27
- Next track - 21
