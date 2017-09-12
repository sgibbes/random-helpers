import subprocess

import wget

'''
mask hansen loss tile with 30% tcd, leaving only loss at 31...100 
'''
tile_id = '00N_110E'
# copy loss tile down from s3
loss_loc = 'http://glad.geog.umd.edu/Potapov/GFW_2016/tiles_2016/{}.tif'
# copy tcd tile down from s3
tcd_loc = 'http://commondatastorage.googleapis.com/earthenginepartners-hansen/GFC2014/Hansen_GFC2014_treecover2000_{}.tif'

loss_tile = '{}_loss.tif'.format(tile_id)
tcd_tile = '{}_tcd.tif'.format(tile_id)

download_dict = {loss_loc: loss_tile, tcd_loc: tcd_tile}

for source, new_name in download_dict.iteritems():
    source = source.format(tile_id)
    new_name = new_name.format(tile_id)
    cmd = ['wget', source, '-o', new_name]
    
    print cmd
    
    subprocess.check_call(cmd)
           
           
# gdal calc statement to create raster of loss at 30

# move up raster to new location on s3

# delete loss and tcd raster

