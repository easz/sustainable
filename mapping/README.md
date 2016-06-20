# Mapping

### Create a heatmap to represent travel duration by public transportation

At the moment umap does not really support a full functional heatmap feature, 
therefore here only a map with colored markers is created for the same purpose.

- Install https://github.com/kennell/schiene to use API accessing http://bahn.de
- Export only 'Transport' layer from http://umap.openstreetmap.fr/en/map/mtn_53474 (i.e. Transport.geojson)
  - Transport layer contains train or bus stations which can be looked up on http://bahn.de
- run check-destination-name.py to check if all station names in Transport.geojson are corrected
- run generate-umap-heatmap-from-train-stations.py to generate Transport.heatmap.geojson
  - by default the travel duration is calculated from Munich main station
  - Transport.heatmap.geojson contains the same feature points from Transport.geojson with color code to represent travel duration
- Import Transport.heatmap.geojson to umap

Example:
![Example](transportation.heatmap.png)