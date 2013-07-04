**tile-utils** is a set of Python scripts for stitching of tiled web maps.

The following sources of web maps are supported:
* Bing Aerial Maps
* Web maps with [OpenStreetMap](http://osm.org) tiling scheme
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

	cd pathTo/tile-utils
	python stitch.py -h

Important note:
If your bounding box definition starts with minus, place -- before it, as in the example below.

Example parameters:

	# Stitching tiles Bing Aerial Maps
	python stitch.py 26.7188,58.3786,26.72067,58.3791 bing
	# Stitching tiles from http://osm.org
	python stitch.py 26.7188,58.3786,26.72067,58.3791 http://{a,b,c}.tile.openstreetmap.org
	# Stitching tiles from a local MBTiles file
	python stitch.py -- -77.0471,38.8790,-77.0299,38.8891 pathTo/fileName.mbtiles

#### Limitation
Only 200 tiles can be downloaded from Bing Aerial Maps or any web map with [OpenStreetMap](http://osm.org) tiling scheme.
You can use [TileMill](http://www.mapbox.com/tilemill/) to produce your own tiles in the [MBTiles](http://www.mbtiles.org) format.