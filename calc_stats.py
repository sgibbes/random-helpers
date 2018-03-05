
import subprocess
import rasterio
import sys

from boto.s3.connection import S3Connection


conn = S3Connection(host="s3.amazonaws.com")
bucket = conn.get_bucket('gfw-files')




def raster_stats(filename):
    path = 's3://gfw-files/sam/carbon_budget/carbon_030218/carbon/{}'.format(filename)
    cmd = ['aws', 's3', 'cp', path, '.']
    subprocess.check_call(cmd)

    with rasterio.open(filename) as src:
        array = src.read()
    try:
        band.min()
    except:
        print "fail"


def tile_list():

    prefix = 'sam/carbon_budget/carbon_030218/carbon/'

    full_path_list = [key.name for key in bucket.list(prefix='{}'.format(prefix))]

    filename_only_list = [x.split('/')[-1] for x in full_path_list]


    return filename_only_list


for tile_id in tile_list():
    raster_stats(tile_id)
