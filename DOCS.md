GpsResponse Object Information
-----

### Properties ###
Description and information copied from [http://catb.org/gpsd/gpsd_json.html](http://catb.org/gpsd/gpsd_json.html).

- **mode**
	- *Description:* Indicates the status of the GPS reception
	- *Availability:* Always
	- *Data Type:* Int
	- *Possible Values:* 0=no mode value yet seen, 1=no fix, 2=2D fix, 3=3D fix
- **sats**
	- *Description:* The number of satellites received by the GPS unit
	- *Availability:* Always
	- *Data Type:* Int
- **lat**
	- *Description:* Latitude in degrees
	- *Availability:* mode >= 2
	- *Data Type:*
	- *Possible Values:* -90.0 to 90.0
- **lon**
	- *Description:* Longitude in degrees
	- *Availability:* mode >= 2
	- *Data Type:* float
	- *Possible Values:* -180.0 to 180.0
- **track**
	- *Description:* Course over ground, degrees from true north
	- *Availability:* mode >= 2
	- *Data Type:* float
- **hspeed**
	- *Description:* Speed over ground, meters per second
	- *Availability:* mode >= 2
	- *Data Type:* float
- **time_iso**
	- *Description:* Time/date stamp in ISO8601 format, UTC. May have a fractional part of up to .001sec precision May be absent if mode is not 2 or 3.
	- *Availability:* mode >= 2
	- *Data Type:* string
	- *Sample Value:* 2016-08-05T01:51:44.000Z
- **error**
	- *Description:* Error information 
		- c - ecp: Climb/sink error estimate in meters/sec, 95% confidence.
		- s - eps: Speed error estinmate in meters/sec, 95% confidence.
		- t - ept: Estimated timestamp error (%f, seconds, 95% confidence). Present if time is present.
		- v - epv: Estimated vertical error in meters, 95% confidence. Present if mode is 3 and DOPs can be calculated from the satellite view.
		- x - epx: Longitude error estimate in meters, 95% confidence. Present if mode is 2 or 3 and DOPs can be calculated from the satellite view.
		- y - epy: Latitude error estimate in meters, 95% confidence. Present if mode is 2 or 3 and DOPs can be calculated from the satellite view.
	- *Availability:* mode >= 2 *(**NOTE:** c & v require mode >= 3)*
	- *Data Type:* dictionary
	- *Possible Values:*
- **alt**
	- *Description:* Altitude in meters
	- *Availability:* mode >= 3
	- *Data Type:* float
- **climb**
	- *Description:* Climb (positive) or sink (negative) rate, meters per second
	- *Availability:* mode >= 3
	- *Data Type:* float

### Methods ###
- **position**
	- *Description:* Get the latitude and longtitude as tuple
	- *Availability:* mode >= 2
	- *Parameters:* None
	- *Return Type:* tuple (latitude, longitude)
	- *Sample Value:*  (39.8333333, -98.585522)
- **speed**
	- *Description:* Get the horisontal speed with the small movements filtered out
	- *Availability:* mode >= 2
	- *Parameters:* None
	- *Return Type:* float
- **position_precision**
	- *Description:* Get the error margin in meters for the current fix
	- *Availability:* mode >= 2
	- *Parameters:* None
	- *Return Type:* tuple (x-y plane, z direction)
- **time**
	- *Description:* Get the GPS time UTC or Local
	- *Availability:* mode >= 2
	- *Parameters:* local_time=False
	- *Return Type:* datetime
- **map_url**
	- *Description:* Get a openstreetmap url for the current position
	- *Availability:* mode >= 2
	- *Parameters:* None
	- *Return Type:* string
	- *Sample Value:* http://www.openstreetmap.org/?mlat=39.8333333&mlon=-98.585522&zoom=15
- **altitude**
	- *Description:* Get the altitude in meters
	- *Availability:* mode >= 3
	- *Parameters:* None
	- *Return Type:* float
- **movement**
	- *Description:* Get the speed and direction of the current movement as dict
	- *Availability:* mode >= 3
	- *Parameters:* None
	- *Return Type:* dictionary
		- speed
		- track
		- climb
- **speed_vertical**
	- *Description:* Get the vertical speed with the small movements filtered out
	- *Availability:* mode >= 3
	- *Parameters:* None
	- *Return Type:* float


Exception Information
-----

- NoFixError: Raised when a value is requested with the mode below the threshold for obtaining the data
	- Needs at least 2D fix
	- Needs at least 3D fix
- General Exceptions
	- Unexpected message received from gps: ...
	- Unexpected data received as welcome. Is the server a gpsd 3 server?


Information on Available Functions
-----

- **connect**
	- *Description:* Connect to a GPSD instance
	- *Parameters:* host="127.0.0.1", port=2947
	- *Return Type:* None
- **get_current**
	- *Description:* Poll gpsd for a new position
	- *Parameters:* None
	- *Return Type:* GpsResponse Object
- **device**
	- *Description:* Get information about current gps device
	- *Parameters:* None
	- *Return Type:* dictionary
		- path
		- speed
		- driver
	- *Sample Data:* {'speed': 9600, 'path': '/dev/ttyS0', 'driver': 'MTK-3301'}


----------

## Sample Code ##

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
