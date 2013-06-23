#!/usr/bin/env python

import os, sqlite3, math, io
from PIL import Image
from base import Base

class Mbtiles(Base):
	maxTileNumber = 1e400
	path = ""
	cursor = None

	def __init__(self, path):
		self.path = path

	def getMaxZoom(self, bbox):
		self.createCursor()
		self.cursor.execute("SELECT MAX(zoom_level) FROM tiles")
		maxZoom = self.cursor.fetchone()[0]
		self.closeCursor()
		return maxZoom

	def doStitching(self, bottom, left, top, right, zoom, resultImage, numTiles):
		self.createCursor()
		tilesetSize = long(math.pow(2, zoom))
		for tile in self.cursor.execute("SELECT tile_column, tile_row, tile_data FROM tiles WHERE zoom_level=? AND tile_column>=? AND tile_column<=? AND tile_row>=? AND tile_row<=?", (zoom, left, right, tilesetSize-bottom-1, tilesetSize-top-1)):
			image = Image.open(io.BytesIO(bytes(tile[2])))
			x = tile[0]
			y = tilesetSize - tile[1] - 1
			resultImage.paste(image, ((x-left)*self.tileWidth, (y-top)*self.tileHeight))
		self.closeCursor()

	def createCursor(self):
		if not self.cursor:
			self.cursor = sqlite3.connect(self.path).cursor()

	def closeCursor(self):
		self.cursor.close()
		self.cursor = None