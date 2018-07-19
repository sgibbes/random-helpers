import geopandas as gpd
import subprocess
import os
import glob


def coords(tile_id):
    NS = tile_id.split("_")[0][-1:]
    EW = tile_id.split("_")[1][-1:]

    if NS == 'S':
        ymax = -1 * int(tile_id.split("_")[0][:2])
    else:
        ymax = int(str(tile_id.split("_")[0][:2]))

    if EW == 'W':
        xmin = -1 * int(str(tile_id.split("_")[1][:3]))
    else:
        xmin = int(str(tile_id.split("_")[1][:3]))

    ymin = str(int(ymax) - 10)
    xmax = str(int(xmin) + 10)

    return str(ymax), str(xmin), ymin, xmax


def create_area_tile(tile):
    tile_id = tile[-8:]

    # get new tile bounds
    uly, ulx, lry, lrx = coords(tile_id)

    # copy down an existing area tile at that latitude
    tile_ns = tile_id.split("_")[0]
    latitude_match = '{0}_080W'.format(tile_ns)

    cmd = ['aws', 's3', 'cp', 's3://gfw2-data/analyses/area_28m/', '.', '--recursive', '--exclude', '*',
           '--include', '*{}*'.format(latitude_match)]
    print '...copying down latitude match'
    subprocess.check_call(cmd)

    latitude_match_file = 'hanson_2013_area_{}.tif'.format(latitude_match)

    dest = 'hanson_2013_area_{}.tif'.format(tile_id)

    # move the matching latitude to the new longitude
    gdal_cmd = ['gdal_translate', '-a_ullr', ulx, uly, lrx, lry, '-co', 'COMPRESS=LZW', latitude_match_file, dest]

    print '...creating new file'
    subprocess.check_call(gdal_cmd)

    return dest


def clean_dir():
    print '...cleaning directory'
    tifs = glob.glob('*.tif*')
    for tif in tifs:
        os.remove(tif)


def upload_file(tif):
    cmd = ['aws', 's3', 'cp', tif, 's3://gfw2-data/analyses/area_28m/']
    print cmd
    print '...uploading to s3'
    subprocess.check_call(cmd)


def main():
    # make list of missing tiles
    global_tiles = gpd.read_file('global_tiles.geojson')
    area_tiles = gpd.read_file('area_tiles.geojson')

    all_tiles = global_tiles['Name'].tolist()
    area_tiles = area_tiles['location'].tolist()

    all_tiles_name = [x[-8:] for x in all_tiles]
    area_tiles_name = [x.strip('.tif')[-8:] for x in area_tiles]

    missing_tiles = list(set(all_tiles_name) - set(area_tiles_name))

    print "Missing {} area tiles".format(len(missing_tiles))

    # create new tiles
    for tile in missing_tiles:
        print "\nCreating area tile for: {}".format(tile[-8:])
        new_area_tile = create_area_tile(tile)
        upload_file(new_area_tile)

        clean_dir()
        print 'DONE'


if __name__ == '__main__':
    main()