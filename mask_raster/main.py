import subprocess
import os
import boto
import glob

import util

def mask_raster(tileid):
    print tileid
    carbon_pool = 'litter' # options: carbon, bgc, deadwood, litter, soil, totalc
    tcd_tif = 'Hansen_GFC2014_treecover2000_{}.tif'
    raster = '{0}_{1}.tif'.format(tileid, carbon_pool)
    thresh = 30
    tcd_tile = 's3://gfw2-data/forest_cover/2000_treecover/{}'.format(tcd_tif)
    raster_tile = 's3://gfw-files/sam/carbon_budget/carbon_030218/{0}/{1}'.format(carbon_pool, raster)
    s3_outfile = 's3://gfw-files/sam/carbon_budget/carbon_030218/30tcd/{}/tif/'.format(carbon_pool)
    failed = False
    # check if masked raster exists
    if not util.check_output_exists(tileid, carbon_pool):
        subprocess.check_call(['touch', '{}_writing.txt'.format(tileid)])
        #copy down tcd tile
        for source in [tcd_tile, raster_tile]:
            print 'downloading {}'.format(source.format(tileid))
            copy_cmd = ['aws', 's3', 'cp', source.format(tileid), '.']
            try:
                subprocess.check_call(copy_cmd)
            except:
                failed = True
        if not failed:
            #mask tcd by 30 and high carbon
            calc = '(A>{}) * B'.format(thresh)
            raster_threshed = raster.replace('.tif', '_{}tcd.tif'.format(thresh))

            outfile = '--outfile={}'.format(raster_threshed)

            cmd = ['gdal_calc.py', '-A', tcd_tif.format(tileid), '-B', raster.format(tileid), '--cal={}'.format(calc)]
            cmd += ['NoDataValue=0', '--co', 'COMPRESS=LZW', '--outfile={}'.format(raster_threshed)]

            print "calculating..."
            subprocess.check_call(cmd)
            print "done!"

            valid_raster = util.get_min_max(raster_threshed)

            if valid_raster:
                #upload to s3
                cmd = ['aws', 's3', 'mv', raster_threshed, s3_outfile]
                subprocess.check_call(cmd)

                write_cmd = ['touch', '{}_good.txt'.format(tileid)]
            else:
                write_cmd = ['touch', '{}_bad.txt'.format(tileid)]
            subprocess.check_call(write_cmd)

            # remove tiles
            tiles = glob.glob('{}*tif*'.format(tileid))

            for tile in tiles:
                os.remove(tile)
    else:
        print "already exists"
        subprocess.check_call(['touch', '{}_exists.txt'.format(tileid)])
