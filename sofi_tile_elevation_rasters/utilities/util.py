import subprocess
from boto.s3.connection import S3Connection
from urlparse import urlparse
import rasterio
import glob
import os

conn = S3Connection(host="s3.amazonaws.com")

def download(s3_path, dest, tifs_only=False):

    cmd = ['aws', 's3', 'cp', s3_path, dest]

    if tifs_only:
        cmd += ['--recursive',  '--exclude', "*", '--include', "*.tif"]

    subprocess.check_call(cmd)

def makevrt(dir):
    cmd = ['gdalbuildvrt', 'tile.vrt', dir + "*.tif"]
    subprocess.check_call(' '.join(cmd), shell=True)


def files_on_s3(s3_dir):
    parsed = urlparse(s3_dir)

    # connect to the s3 bucket
    bucket = conn.get_bucket(parsed.netloc)

    # remove leading slash, for some reason
    prefix = parsed.path[1:]

    # loop through file names in the bucket
    full_path_list = [key.name for key in bucket.list(prefix=prefix)]

    # unpack the filename from the list of files
    filename_only_list = [x.split('/')[-1] for x in full_path_list]
    return filename_only_list

def get_extent(tif):

    dataset = rasterio.open(tif)
    bbox = dataset.bounds

    xmin = str(bbox[0])
    ymin = str(bbox[1])
    xmax = str(bbox[2])
    ymax = str(bbox[3])

    return xmin, ymin, xmax, ymax

def clip_raster(vrt, tcd_tile):


    xmin, ymin, xmax, ymax = get_extent(tcd_tile)
    tile_id = tcd_tile.replace('Hansen_GFC2014_treecover2000_', '')
    print tcd_tile
    print tile_id
    clipped_elevation = tile_id.replace('.tif', '_elevation.tif')
    cmd = ['gdalwarp', '-te', xmin, ymin, xmax, ymax, '-tr', '.00025', '.00025', '-tap']
    cmd += ['-co', 'COMPRESS=LZW', vrt, clipped_elevation]

    subprocess.check_call(cmd)

    return clipped_elevation

def mask_raster(input_tif, tcd_tif):

    calc = '(A>30) * B'
    masked_30tcd = input_tif.replace('.tif', '_30tcd.tif')

    outfile = '--outfile={}'.format(masked_30tcd)

    cmd = ['gdal_calc.py', '-A', tcd_tif, '-B', input_tif, '--cal={}'.format(calc)]
    cmd += ['NoDataValue=255', '--co', 'COMPRESS=LZW', '--outfile={}'.format(masked_30tcd)]

    subprocess.check_call(cmd)

    return masked_30tcd


def upload_to_s3(src, dst):
    cmd = ['aws', 's3', 'cp', src, dst]
    subprocess.check_call(cmd)

def clean_workspace(tile_id):
    tile_id = tile_id.replace('.tif', '')
   
    files = glob.glob('data/tcd/*{}*'.format(tile_id))
    [os.remove(f) for f in files]
    
