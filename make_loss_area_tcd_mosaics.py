import arcpy
import os
import argparse

def main():

    # Parse commandline arguments
    parser = argparse.ArgumentParser(description='make mosaics')
    parser.add_argument('--geodatabase', '-g', required=True, help='path to geodatabase where mosaics will be created')


    args = parser.parse_args()
    for mosaic in ['tcd', 'area', 'loss']:
        print "building mosaic for {}".format(mosaic)
        path_dict = {'tcd': r'S:\treecoverdensity_2000', 'area': r'S:\area_tiles', 'loss': r'S:\lossdata_2001_2014'}
        out_cs = arcpy.SpatialReference(4326)
        arcpy.CreateMosaicDataset_management (args.geodatabase, mosaic, out_cs)

        # add rasters
        mosaic_name = os.path.join(args.geodatabase, mosaic)
        rastype = "Raster Dataset"
        path_to_files = path_dict[mosaic]

        arcpy.AddRastersToMosaicDataset_management(mosaic_name, rastype, path_to_files)
        
if __name__ == "__main__":
    main()