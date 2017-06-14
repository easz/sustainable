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
    hut_data = {}
    with open(INPUT_HUT_JSON) as hut:
        hut_data = json.load(hut)
        hut.close()

    # to hold the result
    hut_layer = {}
    hut_layer["type"] = "FeatureCollection"
    hut_layer["features"] = []

    # parse info
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
