import os
import subprocess




def copydown(tileid, masked_loss_s3):

    tiletocopy = '{0}{1}_loss_at_30tcd.tif'.format(masked_loss_s3, tileid)
    
    cmd = ['aws', 's3', 'cp', tiletocopy, '.']
    
    subprocess.check_call(cmd)

def buildoverviews(tile_path):
    
    cmd = ['gdaladdo', tile_path, '2', '4', '8', '16']

    subprocess.check_call(cmd)
        
def movetos3(tile_path, masked_loss_s3):
    
    cmd = ['aws', 's3', 'mv', tile_path, masked_loss_s3]
    
    subprocess.check_call(cmd)
    
def make_overviews(tileid):

    masked_loss_s3 = 's3://gfw2-data/forest_change/hansen_2016_masked_30tcd/'

    tile_path = '{0}_loss_at_30tcd.tif'.format(tileid)
    copydown(tileid, masked_loss_s3)
    #buildoverviews(tile_path)
    #movetos3(tile_path, masked_loss_s3)
    
    
for tile_id in ['00N_090E', '00N_100E', '00N_110E', '00N_120E', '00N_130E', '10N_090E', '10N_100E', '10N_110E', '10N_120E', '10N_130E']:
    tile_path = r'S:\lossdata_2001_2016\{}.tif'.format(tile_id)
    buildoverviews(tile_path)