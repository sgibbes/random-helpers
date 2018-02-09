import gdal
from gdalconst import GA_ReadOnly
import subprocess
# loop through tile ids to make individual rasters for each 10x10 deg tile id

def coords(tile_id):
    NS = tile_id.split("_")[0][-1:]
    EW = tile_id.split("_")[1][-1:]

    if NS == 'S':
        ymax =-1*int(tile_id.split("_")[0][:2])
    else:
        ymax = int(str(tile_id.split("_")[0][:2]))

    if EW == 'W':
        xmin = -1*int(str(tile_id.split("_")[1][:3]))
    else:
        xmin = int(str(tile_id.split("_")[1][:3]))


    ymin = str(int(ymax) - 10)
    xmax = str(int(xmin) + 10)

    return ymax, xmin, ymin, xmax

def clip_tiles(tile_id):

    out =  r'{}_tiled.tif'.format(tile_id)
    input_raster = r'/Users/sgibbes.local/Documents/Goode_FinalClassification_17_05pcnt_wgs84.tif'

    ymax, xmin, ymin, xmax = coords(tile_id)
    cmd = ['gdalwarp', '-tr', '.00025', '.00025',  '-ot', 'Byte', '-co', 'COMPRESS=LZW', '-tap', input_raster, out, '-te', str(xmin), str(ymin), str(xmax), str(ymax)]
    subprocess.check_call(cmd)

    cmd = ['aws', 's3', 'cp', out, 's3://gfw-files/sam/carbon_budget/data_inputs2/tsc_model/']
    subprocess.check_call(cmd)
