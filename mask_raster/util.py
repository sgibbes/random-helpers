from boto.s3.connection import S3Connection

conn = S3Connection(host="s3.amazonaws.com")
bucket = conn.get_bucket('gfw-files')

from osgeo import gdal


def check_output_exists(tileid, carbon_pool):

    prefix = 'sam/carbon_budget/carbon_030218/30tcd/{}/tif/'.format(carbon_pool)

    full_path_list = [key.name for key in bucket.list(prefix='{}'.format(prefix))]

    filename_only_list = [x.split('/')[-1] for x in full_path_list]
    carbon_tile = '{0}_{1}_30tcd.tif'.format(tileid, carbon_pool)

    return carbon_tile in filename_only_list

def get_min_max(tif):
    gtif = gdal.Open(tif)
    srcband = gtif.GetRasterBand(1)
    stats = srcband.GetStatistics(True, True)
    min_val = stats[0]
    max_val = stats[1]

    if min_val >= 0 and max_val < 1000:
        valid_raster = True
    else:
        valid_raster = False

    return valid_raster
