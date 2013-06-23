#!/usr/bin/env python

import sys, string, urllib2, math, logging
import util
from base import Base

digs = string.digits + string.lowercase
def int2base(x, base):
	if x < 0: sign = -1
	elif x==0: return '0'
	else: sign = 1
	x *= sign
	digits = []
	while x:
		digits.append(digs[x % base])
		x /= base
	if sign < 0:
		digits.append('-')
	digits.reverse()
	return ''.join(digits)

class BingAerial(Base):
	metadataPath = "http://dev.virtualearth.net/REST/v1/Imagery/Metadata/Aerial"
	bingMapsKey = ""
	imageUrl = ""
	imageUrlSubdomains = None
	zoomMax = 21 # max zoom for the whole world
	
	def __init__(self):
		# reading bing maps key
		self.bingMapsKey = open("bing_maps_key.txt", "r").read()
		self.getMetadata()

	def getMetadata(self):
		response = util.fetchJson("%s?key=%s" % (self.metadataPath, self.bingMapsKey))
		if "errorDetails" not in response:
			data = response["resourceSets"][0]["resources"][0]
			self.tileWidth = data["imageWidth"]
			self.tileHeight = data["imageHeight"]
			self.imageUrl = data["imageUrl"]
			self.imageUrlSubdomains = data["imageUrlSubdomains"]
			self.zoomMax = data["zoomMax"]
			self.numSubdomains = len(self.imageUrlSubdomains)
		else:
			logging.error("Unknown response from the server")
			sys.exit(-1)

	def getTileUrl(self, zoom, x, y, tileCounter):
		# calculating quadkey
		interleaved = [None]*2*zoom
		interleaved[::2] = bin(y)[2:].zfill(zoom)
		interleaved[1::2] = bin(x)[2:].zfill(zoom)
		interleaved = ''.join(interleaved)
		# converting to decimal
		interleaved = int(interleaved, 2)
		# converting to base 4
		quadkey = int2base(interleaved, 4).zfill(zoom)
		url = self.imageUrl.replace("{subdomain}", self.imageUrlSubdomains[tileCounter % self.numSubdomains])
		url = url.replace("{quadkey}", quadkey)
		return url
	
	def getMaxZoom(self, bbox):
		(bottom, left) = util.toSphMercator(bbox[0], bbox[1])
		(top, right) = util.toSphMercator(bbox[2], bbox[3])
		(centerY, centerX) = util.toGeographic((top+bottom)/2, (left+right)/2)
		zoom = self.zoomMax
		while True:
			response = util.fetchJson("%s/%s,%s?zl=%s&key=%s" % (self.metadataPath, centerY, centerX, zoom, self.bingMapsKey))
			if "errorDetails" not in response:
				data = response["resourceSets"][0]["resources"][0]
				if data["vintageEnd"]: break
			else:
				logging.error("Unknown response from the server")
				sys.exit(-1)
			zoom = zoom-1
		return zoom

	def getTileImage(self, zoom, x, y, counter):
		url = self.getTileUrl(zoom, x, y, counter)
		try:
			tile = urllib2.urlopen(url).read()
		except Exception, e:
			# Something went wrong
			logging.error(e)
			logging.error("Unable to download image %s" % url)
			sys.exit(-1)
		return tile