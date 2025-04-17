# UStall GitHub

**table of contents**

[[_TOC_]]

## Hardware SetUP

1. Plug in USB to UART converter
2. Plug in XBOX controller
3. Plug in ethernet cable (Note: Ethernet cable has to be crimped as only the pins needed for 100BASE-T)

## Software SetUP

1. Go to view network connections
2. Go to ethernet adapter properties
3. Got to IPv4 settings
4. Change IP address to manually
5. Set IP address to: 192.168.0.5
6. Set subnet mask to: 255.255.255.0
7. Go to PuTTY and connect to 192.168.0.3
8. User: julia password: s
9. start motion with cmd: sudo motion
10. Open 192.168.0.3:8070 on the PC to view the cameras
11. Go to the device manager and figure out which COM the UART bridge is
12. Start the UStallGUI
13. To connect to the ROV specify the right COM port
14. Change tab to controllers
15. Search for controllers
16. Connect to controller

## Matlab

Code for Matlab used to Model the ROV
[README](Matlab/README.md)

## Pico-LouisControlEngine

Code for controlling the thrusters
[README](Pico-LouisControlEngine/README.md)

## UStallGUI

Code for the GUI
[README](UStallGUI/README.md)

## RaspberryPI

Code for the RaspberryPI
[README](RaspberryPI/README.md)

## Changelog

- **17 April 2025**: Initial version of the document.
