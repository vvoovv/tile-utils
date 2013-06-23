#!/usr/bin/env python

import sys, urllib2, logging
from base import Base

class OsmTiles(Base):
	maxZoom = 18
	url = ""
	subdomains = None
	url1 = "" # url1 and url2 are url parts if subdomains are provided
	url2 = ""

	def __init__(self, url):
		# checking if url contains subdomains
		leftBracketPosition = url.find("{")
		rightBracketPosition = url.find("}")
		if leftBracketPosition != -1 and rightBracketPosition != -1:
			self.subdomains = url[leftBracketPosition+1:rightBracketPosition].split(",")
			self.numSubdomains = len(self.subdomains)
			self.url1 = url[:leftBracketPosition]
			self.url2 = url[rightBracketPosition+1:]
		else:
			self.url = url

	def getTileUrl(self, zoom, x, y, tileCounter):
		url = None
		if self.subdomains:
			url = "%s%s%s" % (self.url1, self.subdomains[tileCounter % self.numSubdomains], self.url2)
		else:
			url = self.url
		url = "%s/%s/%s/%s.png" % (url, zoom, x, y)
		return url

	def getMaxZoom(self, bbox):
		return self.maxZoom

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