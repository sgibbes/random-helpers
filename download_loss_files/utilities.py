# download the loss tiles for a particular tile id
import urllib
import sys
import subprocess
import os
import argparse


dirname, filename = os.path.split(os.path.abspath(__file__))

def make_mosaic(data_type_list):

    import arcpy
    print "creating mosaic"
    # create geodatabase
    gdb_name = 'mosaics.gdb'
    if not arcpy.Exists(os.path.join(dirname,gdb_name)):
        arcpy.CreateFileGDB_management(dirname, gdb_name)
    
    for data_type in data_type_list:
    
            # create mosaic
            out_cs = arcpy.SpatialReference(4326)
            mosaic = os.path.join(gdb_name, data_type)
            if not arcpy.Exists(mosaic):
                arcpy.CreateMosaicDataset_management (gdb_name, data_type, out_cs)

            # add rasters
            mosaic_name = os.path.join(gdb_name, data_type)
            rastype = "Raster Dataset"
            path_to_files = os.path.join(dirname, data_type)

            arcpy.AddRastersToMosaicDataset_management(mosaic_name, rastype, path_to_files)
            
            
def download_url(url_source, tile_id, name):
    if not os.path.exists(os.path.join(dirname, name)):
        os.mkdir(os.path.join(dirname, name))
    url_dest = os.path.join(dirname, name, '{0}_{1}.tif'.format(tile_id, name))
    print "downloading {0} for {1}".format(name, tile_id)
    urllib.urlretrieve(url_source, url_dest)
    
def download_aws(source, tile_id, name):
    if not os.path.exists(os.path.join(dirname, name)):
        os.mkdir(os.path.join(dirname, name))
    dest = os.path.join(dirname, name, '{1}_{0}.tif'.format(name, tile_id))
    cmd = ['aws', 's3', 'cp', source, dest]
    print "downloading {0} for {1}".format(name, tile_id)
    subprocess.check_call(cmd)

def download_tiles(args):

    data_type_list = [] # list of data to download, and storing it for if user wants to make mosaics
    tile_id = args.tile_id
    loss = args.loss
    tcd = args.tcd
    area = args.area
    biomass = args.biomass
    create_mosaic = args.create_mosaic
    
    file_source_dict = {'loss':'https://storage.googleapis.com/earthenginepartners-hansen/GFC-2015-v1.3/Hansen_GFC-2015-v1.3_lossyear_{}.tif', 'tcd':'https://storage.googleapis.com/earthenginepartners-hansen/GFC-2015-v1.3/Hansen_GFC-2015-v1.3_treecover2000_{}.tif', 'biomass': 's3://WHRC-carbon/global_27m_tiles/final_global_27m_tiles/biomass_10x10deg/{}_biomass.tif', 'area': 's3://gfw2-data/analyses/area_28m/hanson_2013_area_{}.tif'}
    
    # loss tile:
    if loss:

        url_source = file_source_dict['loss']
        download_url(url_source, tile_id, 'loss')
        data_type_list.append('loss')
        
    # tcd tile
    if tcd:
    
        url_source = file_source_dict['tcd']
        download_url(url_source, tile_id, 'tcd')
        data_type_list.append('tcd')
        
    # biomass tile
    if biomass:
    
        url_source = file_source_dict['biomass']
        download_aws(source, tile_id, 'biomass')
        data_type_list.append('biomass')
        
    # area tile
    if area:
    
        url_source = file_source_dict['area']
        download_aws(source, tile_id, 'area')
        data_type_list.append('area')
    
    
    return data_type_list