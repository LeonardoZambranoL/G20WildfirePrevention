import rasterio
import rasterio.features
import rasterio.warp
import json


def trasnform_tif_to_geojson(filename,destination_file_directory) :
    with rasterio.open(filename) as dataset:

        # Read the dataset's valid data mask as a ndarray.
        mask = dataset.dataset_mask()

        # Extract feature shapes and values from the array.
        for geom, val in rasterio.features.shapes(
                mask, transform=dataset.transform):

            # Transform shapes from the dataset's own coordinate
            # reference system to CRS84 (EPSG:4326).
            geom = rasterio.warp.transform_geom(
                dataset.crs, 'EPSG:4326', geom, precision=6)

            # Print GeoJSON shapes to stdout.
            with open(destination_file_directory, 'a') as file:
            # Use json.dump() to write the data to the file as a single line
                json.dump(geom,file)
                file.write('\n')
                
                


