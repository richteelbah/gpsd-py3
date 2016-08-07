#!/usr/bin/env python3

import gpsd
import sys

# Connect to the local gpsd
gpsd.connect()

# Connect somewhere else
gpsd.connect()

# Get gps position
try:
    packet = gpsd.get_current()
except Exception as e:
    print("ERROR: Error occured while parsing JSON or expected key or attribute missing")
    sys.exit()

# See the inline docs for GpsResponse for the available data
print(" ************ PROPERTIES ************* ")
print("              Mode: {}".format(packet.mode))
print("        Satellites: {}".format(packet.sats))
if packet.mode >= 2:
    print("          Latitude: {}".format(packet.lat))
    print("         Longitude: {}".format(packet.lon))
    print("             Track: {}".format(packet.track))
    print("  Horizontal Speed: {}".format(packet.hspeed))
    print("              Time: {}".format(packet.time_iso))
    print("             Error: {}".format(packet.error))
else:
    print("          Latitude: NOT AVAILABLE")
    print("         Longitude: NOT AVAILABLE")
    print("             Track: NOT AVAILABLE")
    print("  Horizontal Speed: NOT AVAILABLE")
    print("             Error: NOT AVAILABLE")
    
if packet.mode >= 3:
    print("          Altitude: {}".format(packet.alt))
    print("             Climb: {}".format(packet.climb))
else:
    print("          Altitude: NOT AVAILABLE")
    print("             Climb: NOT AVAILABLE")

print(" ************** METHODS ************** ")
if packet.mode >= 2:
    print("          Location: {}".format(packet.position()))
    print("             Speed: {}".format(packet.speed()))
    print("Position Precision: {}".format(packet.position_precision()))
    print("          Time UTC: {}".format(packet.time()))
    print("        Time Local: {}".format(packet.time(local_time=True)))
    print("           Map URL: {}".format(packet.map_url()))
else:
    print("          Location: NOT AVAILABLE")
    print("             Speed: NOT AVAILABLE")
    print("Position Precision: NOT AVAILABLE")
    print("          Time UTC: NOT AVAILABLE")
    print("        Time Local: NOT AVAILABLE")
    print("           Map URL: NOT AVAILABLE")
    
if packet.mode >= 3:
    print("          Altitude: {}".format(packet.altitude()))
    print("          Movement: {}".format(packet.movement()))
    print("      Speed Vertical: {}".format(packet.speed_vertical()))
else:
    print("          Altitude: NOT AVAILABLE")
    print("          Movement: NOT AVAILABLE")
    print("     Speed Vertical: NOT AVAILABLE")

print(" ************* FUNCTIONS ************* ")
print("            Device: {}".format(gpsd.device()))
