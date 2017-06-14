#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# create sort-of heatmap on umap
import os
import sys
import re
import json
from optparse import OptionParser

#
# command arguments / options
# Example:
# 		%prog *.json
#
parser = OptionParser(usage="usage: %prog file1.json file2.json ...")
(options, args) = parser.parse_args()

if len(args) == 0:
    parser.print_help()
    sys.exit()

for filename in args:
    INPUT_HUT_JSON = filename
    OUTPUT_HUT_LAYER_GEOJSON = '%s.geojson' % os.path.splitext(filename)[0]
    print "converting %s to %s" % (INPUT_HUT_JSON, OUTPUT_HUT_LAYER_GEOJSON)

    # to hold the source
    src_data = {}
    with open(INPUT_HUT_JSON) as src:
        src_data = json.load(src)
        src.close()

    # to hold the source elements
    data_entries = src_data["elements"]

    # parse node with lat/lon
    lat_lon_lookup = {}
    for entry in data_entries:
        entry_type = entry["type"]
        entry_id = entry["id"]
        if entry_type == "node":
            lat_lon_lookup[entry_id] = {}
            lat_lon_lookup[entry_id]["lat"] = entry["lat"]
            lat_lon_lookup[entry_id]["lon"] = entry["lon"]
    for entry in data_entries:
        entry_type = entry["type"]
        entry_id = entry["id"]
        if entry_type == "way":
            lat_lon_lookup[entry_id] = {}
            ref_id = entry["nodes"][0]
            lat_lon_lookup[entry_id]["lat"] = lat_lon_lookup[ref_id]["lat"]
            lat_lon_lookup[entry_id]["lon"] = lat_lon_lookup[ref_id]["lon"]

    # to hold the layer data
    hut_layer = {}
    hut_layer["type"] = "FeatureCollection"
    hut_layer["features"] = []

    for entry in data_entries:
        entry_type = entry["type"]
        entry_id = entry["id"]

        if "tags" not in entry:
            continue

        hut_tags = entry["tags"]
        hut_name = "unknown"
        if "name" in hut_tags:
            hut_name = hut_tags["name"]
        hut_website = ""
        if "website" in hut_tags:
            hut_website = hut_tags["website"]

        hut_lon = ""
        hut_lat = ""

        if entry_type == "node":
            hut_lon = entry["lon"]
            hut_lat = entry["lat"]
        elif entry_type == "way":
            hut_lon = lat_lon_lookup[entry_id]["lon"]
            hut_lat = lat_lon_lookup[entry_id]["lat"]
        elif entry_type == "relation":
            ref_id = entry["members"][0]["ref"]
            hut_lon = lat_lon_lookup[ref_id]["lon"]
            hut_lat = lat_lon_lookup[ref_id]["lat"]
        else:
            print "Unknown type: ", entry_type, " id: ", entry_id
            continue

        # add feature in the layer
        feature = {}
        feature["type"] = "Feature"
        feature["geometry"] = {}
        feature["geometry"]["type"] = "Point"
        feature["geometry"]["coordinates"] = [hut_lon, hut_lat]
        feature["properties"] = {}
        feature["properties"]["_storage_options"] = {}
        feature["properties"]["_storage_options"]["iconClass"] = "Circle"
        feature["properties"]["_storage_options"]["color"] = "DarkBlue"
        feature["properties"]["name"] = hut_name
        feature["properties"]["description"] = hut_website
        hut_layer["features"].append(feature)

    # output
    with open(OUTPUT_HUT_LAYER_GEOJSON, 'w') as outfile:
        json.dump(hut_layer, outfile, indent=2)
        outfile.close()
