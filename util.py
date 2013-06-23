#!/usr/bin/env python

import math, urllib2, json

earthRadius = 6378137

def toSphMercator(lat, lon):
	return (
		earthRadius * math.log(math.tan(math.pi/4 + lat*math.pi/360)),
		earthRadius * lon * math.pi / 180
	)

def toGeographic(y, x):
	return (
		360/math.pi * math.atan(math.exp(y/earthRadius)) - 90,
		180*x/(math.pi*earthRadius)
	)

def toTileCoords(lat, lon, zoom):
	halfEquator = math.pi * earthRadius
	equator = 2 * halfEquator
	numTiles = math.pow(2, zoom)
	
	(lat, lon) = toSphMercator(lat, lon)
	# moving zero to the top left corner
	lat = halfEquator - lat
	lon = lon + halfEquator
	y = lat * numTiles / equator
	x = lon * numTiles / equator
	return (int(math.floor(y)), int(math.floor(x)))

def fetchJson(url):
	try:
		return json.loads(
			urllib2.urlopen(url).read()
		)
	except urllib2.URLError as e:
		if hasattr(e, "reason"):
			logging.error("Failed to reach the server: %s" % e.reason)
		elif hasattr(e, "code"):
			logging.error("Server error: %s" % e.code)
		sys.exit(-1)
	except:
		logging.error("JSON error")
