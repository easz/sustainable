# -*- coding: utf-8 -*-
#!/usr/bin/env python3

# check if station name is the same as in bahn.de page

import json
import schiene
import time

INPUT_TRANSPORT_LAYER_GEOJSON = 'Transport.geojson'

# Bahn.de API by https://github.com/kennell/schiene
api = schiene.Schiene()

# to parse geojson file from the exported ''Transport'' layer of http://umap.openstreetmap.fr/en/map/mtn_53474
transportation_data = {}
with open(INPUT_TRANSPORT_LAYER_GEOJSON) as transportation:    
    transportation_data = json.load(transportation)

# parse station name and coordinates
stations = transportation_data["features"]
for station in stations:
	# station coordinate
	[longitude, latitude] = station["geometry"]["coordinates"]
	# station name
	station_name = station["properties"]["name"].strip() 

	# get official name from bahn.de
	official_station_name = api.stations(station_name)[0]["value"]

	if station_name != official_station_name:
		print "[WARN]", station_name, "<-?->", official_station_name
	else:
		print "[OK]", station_name

	# relax a bit
	time.sleep(1)