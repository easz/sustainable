#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# create sort-of heatmap on umap

import json
import schiene
import time
import random

OUTPUT_TRANSPORT_HEATMAP_LAYER_GEOJSON = 'Transport.heatmap.geojson'
INPUT_TRANSPORT_LAYER_GEOJSON = 'Transport.geojson'
CALCULATE_FROM_STATION = u'München Hbf'

COLOR_CODE = {}
COLOR_CODE[31] = "LawnGreen"
COLOR_CODE[61] = "Green"
COLOR_CODE[91] = "GoldenRod"
COLOR_CODE[121] = "SaddleBrown"
COLOR_CODE[151] = "DeepPink"
COLOR_CODE[181] = "DarkViolet"
COLOR_CODE[211] = "DimGrey"


######################
'''return both "time string" in hh:mm and "time in minutes" from the API result https://github.com/kennell/schiene'''
def findTheShortestTime(conns): #program does nothing as written
	shortest = 9999999999
	shortest_time_string = ""
	for c in conns:
		time_string_hh_mm = c["time"]
		hh, mm = map(int, time_string_hh_mm.split(':'))
		num = hh * 60 + mm
		if num < shortest:
			shortest = num
			shortest_time_string = time_string_hh_mm
	return shortest_time_string, shortest
######################


# Bahn.de API by https://github.com/kennell/schiene
api = schiene.Schiene()

# to parse geojson file from the exported ''Transport'' layer of http://umap.openstreetmap.fr/en/map/mtn_53474
transportation_data = {}
with open(INPUT_TRANSPORT_LAYER_GEOJSON) as transportation:    
    transportation_data = json.load(transportation)

# to hold the result
transportation_heatmap_layer = {}
transportation_heatmap_layer["type"] = "FeatureCollection"
transportation_heatmap_layer["features"] = []

# debug info
api_debug=open('./api_debug', 'w')

# parse station name and coordinates
stations = transportation_data["features"]
for station in stations:
	# station coordinate
	[longitude, latitude] = station["geometry"]["coordinates"]

	# station name
	station_name = station["properties"]["name"].strip() 

	# FIXME: search for week days or weekend. search for early morning and late evening
	conn = api.connections(CALCULATE_FROM_STATION, station_name)	
	print >> api_debug, repr(station_name)
	print >> api_debug, json.dumps(conn, indent=2)

	time_string_hh_mm = ""
	time_color = "Black"
	if len(conn) > 0:
		time_string_hh_mm, num = findTheShortestTime(conn)
		time_color = COLOR_CODE.get(num, COLOR_CODE[min(COLOR_CODE.keys(), key=lambda k: abs(k-num))])
		print "[OK]", station_name, " ", time_string_hh_mm
	else:
		print "[ERROR]", station_name

	feature = {}
	feature["type"] = "Feature"
	feature["geometry"] = {}
	feature["geometry"]["type"] = "Point"
	feature["geometry"]["coordinates"] = [longitude, latitude]
	feature["properties"] = {}
	feature["properties"]["_storage_options"] = {}
	feature["properties"]["_storage_options"]["iconClass"] = "Circle"
	feature["properties"]["_storage_options"]["color"] = time_color
	feature["properties"]["name"] = station_name
	feature["properties"]["description"] = time_string_hh_mm + u' from ' + CALCULATE_FROM_STATION
	transportation_heatmap_layer["features"].append(feature)

	# relax a bit
	time.sleep(1)

with open(OUTPUT_TRANSPORT_HEATMAP_LAYER_GEOJSON, 'w') as outfile:
    json.dump(transportation_heatmap_layer, outfile, indent=2)