import subprocess

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
    
    
def iterate_tiles(tile_id):

    print "running: {}".format(tile_id)
    ymax, xmin, ymin, xmax = coords(tile_id)
    rasterize = ['gdal_rasterize', '-co', 'COMPRESS=LZW', '-tr', '0.00025', '0.00025', '-ot',
                             'Byte', '-a', 'LC2000', '-a_nodata', '0', '-te', str(xmin), str(ymin), str(xmax), str(ymax), '-tap', 'inshape.shp', 'outraster.tif']
                             
    subprocess.check_call(rasterize)