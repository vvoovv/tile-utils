**tile-utils** is a set of Python scripts for stitching of tiled web maps.

The following sources of web maps are supported:
* Bing Aerial Maps
* Web maps with [OpenStreetMap](http://osm.org) alike tiling scheme
* [MBTiles](http://www.mbtiles.org) local files

#### Possible applications
* Preparing a big map for printing
* Making a field paper for a painting program in your mobile device

#### Prerequisites
* Python 2.7
* Python Imaging Library ([PIL](http://www.pythonware.com/products/pil/))

#### Installation
* [Download](https://github.com/vvoovv/tile-utils/archive/master.zip) and unpack ZIP archive
* Replace the content of *bing_maps_key.txt* with your Bing Maps Key. See the [instructions](http://msdn.microsoft.com/en-us/library/ff428642.aspx) how to get a Bing Maps Key

#### Usage
See

	python stitch.py -h
Example parameters

	# Stitching tiles Bing Aerial Maps
	python stitch.py 58.3786,26.7188,58.3791,26.72067 bing
	# Stitching tiles from http://osm.org
	python stitch.py 58.3786,26.7188,58.3791,26.72067 http://{a,b,c}.tile.openstreetmap.org
	# Stitching tiles from a local MBTiles file
	python stitch.py 38.8790,-77.0471,38.8891,-77.0299 pathTo/fileName.mbtiles