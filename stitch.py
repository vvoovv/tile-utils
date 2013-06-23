#!/usr/bin/env python

# Example parameters
# stitch.py 58.3786,26.7188,58.3791,26.72067 bing
# stitch.py 58.3786,26.7188,58.3791,26.72067 http://{a,b,c}.tile.openstreetmap.org
# stitch.py 38.8790,-77.0471,38.8891,-77.0299 ..\tiles.mbtiles

import sys, os, argparse, logging

from bing_aerial import BingAerial
from osm_tiles import OsmTiles
from mbtiles import Mbtiles

parser = argparse.ArgumentParser()
parser.add_argument("bbox", help="area bbox coordinates in the form bottom,left,top,right; example: 58.3786,26.7188,58.3791,26.72067")
parser.add_argument("source", help="source for tiles; example values: bing, http://{a,b,c}.tile.openstreetmap.org")
parser.add_argument("-z", "--zoom", type=int, help="desired zoom")
parser.add_argument("-o", "--output", help="result image name, extension (.png or .jpg) defines image format type")
args = parser.parse_args()

# preparing bbox
bbox = [float(i) for i in args.bbox.split(",")]

if args.source == "bing":
	tiles = BingAerial()
elif len(args.source)>7 and args.source[:7] == "http://":
	tiles = OsmTiles(args.source)
elif len(args.source)>8 and os.path.isfile(args.source) and args.source[-8:] == ".mbtiles":
	tiles = Mbtiles(args.source)
else:
	logging.error("Unknown tile source")
	sys.exit(-1)

tiles.stitch(bbox, args.zoom, output=args.output)
