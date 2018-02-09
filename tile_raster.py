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

    out =  r'U:\sgibbes\loss_idn_moef\idn_primary.tif.aux\{}_idn_prf.tif'.format(tile_id)
    input_raster = r'U:\sgibbes\loss_idn_moef\idn_primary.tif.aux\idn_primary.tif'

    ymax, xmin, ymin, xmax = coords(tile_id)
    cmd = ['gdalwarp', '-tr', '.00025', '.00025',  '-co', 'COMPRESS=LZW', '-tap', input_raster, out, '-te', str(xmin), str(ymin), str(xmax), str(ymax), '-t_srs', 'EPSG:4326']  
    subprocess.check_call(cmd)
    
    
for tile_id in ['00N_090E', '00N_100E', '00N_110E', '00N_120E', '00N_130E', '00N_140E', '10N_090E', '10N_100E', '10N_120E', '10N_130E']:
    clip_tiles(tile_id)