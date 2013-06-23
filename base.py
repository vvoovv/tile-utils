#!/usr/bin/env python

import sys, io, logging, datetime
from PIL import Image
import util

class Base():
	maxTileNumber = 200
	tileWidth = 256
	tileHeight = 256
	numSubdomains = 0

	def stitch(self, bbox, zoom, **kwargs):
		if zoom is None:
			# finding max zoom for the central tile
			zoom = self.getMaxZoom(bbox)
		# converting bottom-left and top right points of bbox to tile coords
		(bottom, left) = util.toTileCoords(bbox[0], bbox[1], zoom)
		(top, right) = util.toTileCoords(bbox[2], bbox[3], zoom)
		# calculating number of tiles
		numXtiles = right-left+1
		numYtiles = bottom-top+1
		numTiles = numXtiles*numYtiles
		if (numTiles>self.maxTileNumber):
			logging.error("Maximum number of tiles (%s) is exceeded" % self.maxTileNumber)
			sys.exit(-1)

		# downloading tiles and composing result image
		resultImage = Image.new("RGBA", (numXtiles*self.tileWidth, numYtiles*self.tileHeight), (0,0,0,0))
		self.doStitching(bottom, left, top, right, zoom, resultImage, numTiles)
		if kwargs["output"]:
			outputFileName = kwargs["output"]
		else:
			outputFileName = self.getOutputFileName()
		resultImage.save(outputFileName)

	def getOutputFileName(self):
		now = datetime.datetime.now()
		return "%d%02d%02d%02d%02d%02d.png" % (now.year, now.month, now.day, now.hour, now.minute, now.second)

	def doStitching(self, bottom, left, top, right, zoom, resultImage, numTiles):
		# downloading tiles and composing result image
		counter = 0
		for x in range(left, right+1):
			for y in range(top, bottom+1):
				print "processing image %s out of %s" % (counter+1, numTiles)
				tile = self.getTileImage(zoom, x, y, counter)
				image = Image.open(io.BytesIO(tile))
				resultImage.paste(image, ((x-left)*self.tileWidth, (y-top)*self.tileHeight))
				counter += 1