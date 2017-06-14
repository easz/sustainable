#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# create sort-of heatmap on umap

import json

INPUT_HUT_JSON = 'Hut.France.json'
OUTPUT_HUT_LAYER_GEOJSON = 'Hut.France.geojson'

hut_data = {}
with open(INPUT_HUT_JSON) as hut:    
  hut_data = json.load(hut)

# to hold the result
hut_layer = {}
hut_layer["type"] = "FeatureCollection"
hut_layer["features"] = []


# parse station name and coordinates
huts = hut_data["elements"]
for hut in huts:
  #hut_type = hut["type"]
  hut_lat = hut["lat"]
  hut_lon = hut["lon"]
  hut_tags = {}
  hut_name = ""
  hut_website = ""
  if "tags" in hut:
    hut_tags = hut["tags"]
  if "name" in hut_tags:
    hut_name = hut_tags["name"]
  if "website" in hut_tags:
    hut_website = hut_tags["website"]
  
  feature = {}
  feature["type"] = "Feature"
  feature["geometry"] = {}
  feature["geometry"]["type"] = "Point"
  feature["geometry"]["coordinates"] = [hut_lon, hut_lat]
  feature["properties"] = {}
  feature["properties"]["_storage_options"] = {}
  feature["properties"]["_storage_options"]["iconClass"] = "Circle"
  feature["properties"]["_storage_options"]["color"] = "DarkViolet"
  feature["properties"]["name"] = hut_name
  feature["properties"]["description"] = hut_website
  hut_layer["features"].append(feature)


with open(OUTPUT_HUT_LAYER_GEOJSON, 'w') as outfile:
  json.dump(hut_layer, outfile, indent=2)
