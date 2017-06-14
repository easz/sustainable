# Mapping

### Make a map with umap

A map http://u.osmfr.org/m/53474/ is created to collect hiking and climbing destination around Munich.
Their closest train or bus stations are also marked in the map.

### Create a map to represent alpine huts

- [Query alpine_hut from OSM](http://overpass-turbo.eu/s/pLp)

### Create a heatmap to represent travel duration by public transportation

At the moment umap does not really support a full functional heatmap feature,
therefore here only a map with colored markers is created for the same purpose.

- Install https://github.com/kennell/schiene to use API accessing http://bahn.de
- Export only 'Transport' layer from http://umap.openstreetmap.fr/en/map/mtn_53474 (i.e. Transport.geojson)
  - Transport layer contains train or bus stations and their names should be consistent with http://bahn.de
  - run Transport/check-destination-name.py to check if all station names in Transport.geojson are corrected
- run Transport/generate-umap-heatmap-from-train-stations.py to generate Transport.heatmap.geojson
  - by default the travel duration is calculated from Munich main station
  - Eventually the generated Transport.heatmap.geojson needs to be edited manually in case of something wrong.
  - Transport.heatmap.geojson contains the same feature points from Transport.geojson with color code to represent travel duration
- Import Transport.heatmap.geojson to umap

Example:

![Example](Transport/transportation.heatmap.png)

Color code:
- green-ish: < 1h
- yelloe/brown-ish: < 2h
- purple/pink-ish: < 3h
- grey: > 3h
- black: info not available at this time point
