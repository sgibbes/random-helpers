import multiprocessing
import os

from utilities import util, mask_tiles

for dir in ['data/elevation', 'data/tcd']:
    
    if not os.path.exists(dir):
        
        os.makedirs(dir)
  
        
# download elevation rasters
s3_path = 's3://gfw-files/state_of_forest/indicator_data/elevation_raster/'
util.download(s3_path, 'data/elevation/', True)

# build vrt of elevation rasters
vrt = util.makevrt('data/elevation/')

# connect to tcd tiles on s3 and download each one
tcd_tiles = util.files_on_s3('s3://gfw2-data/forest_cover/2000_treecover/')

# clip and mask elevation data to 30% tcd
for tcd_tile in tcd_tiles:
    mask_tiles.mask_tiles(tcd_tile)

if __name__ == '__main__':
    count = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=count-2)
    pool.map(mask_tiles.mask_tiles, tcd_tiles)
