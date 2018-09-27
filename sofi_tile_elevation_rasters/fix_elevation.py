import glob
import subprocess

elevation_tiles = glob.glob('data/elevation/*.tif')

for t in elevation_tiles:
    
    cmd = ['gdalwarp', t, 'data/elevation_byte/{}'.format(t.split('/')[-1]), '-ot', 'Byte']
    print cmd
    subprocess.check_call(cmd)
