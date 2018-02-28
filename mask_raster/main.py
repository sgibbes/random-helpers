import subprocess
import os

def mask_raster(tileid):

    tcd_tif = 'Hansen_GFC2014_treecover2000_{}.tif'
    raster = '{}_carbon.tif'.format(tileid)
    thresh = 30
    tcd_tile = 's3://gfw2-data/forest_cover/2000_treecover/{}'.format(tcd_tif)
    raster_tile = 's3://gfw-files/sam/carbon_budget/carbon_011018/carbon/{}'.format(raster)
    s3_outfile = 's3://gfw-files/sam/carbon_budget/carbon_011018/30tcd/carbon/tif/'
    #copy down tcd tile
    for source in [tcd_tile, raster_tile]:
        print 'downloading {}'.format(source.format(tileid))
        copy_cmd = ['aws', 's3', 'cp', source.format(tileid), '.']

        subprocess.check_call(copy_cmd)

    #mask tcd by 30 and high carbon
    calc = '(A>{}) * B'.format(thresh)
    raster_threshed = raster.replace('.tif', '_{}tcd.tif'.format(thresh))

    outfile = '--outfile={}'.format(raster_threshed)

    cmd = ['gdal_calc.py', '-A', tcd_tif.format(tileid), '-B', raster.format(tileid), '--cal={}'.format(calc)]
    cmd += ['NoDataValue=255', '--co', 'COMPRESS=LZW', '--outfile={}'.format(raster_threshed)]

    print "calculating..."
    subprocess.check_call(cmd)
    print "done!"

    #upload to s3
    cmd = ['aws', 's3', 'mv', raster_threshed, s3_outfile]
    subprocess.check_call(cmd)

    # remove tiles
    for tile in [tcd_tif.format(tileid), raster]:
        os.remove(tile)
