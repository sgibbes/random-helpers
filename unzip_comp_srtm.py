import subprocess
import zipfile
import os
import glob
import shutil

def unzipfiles(myzipfile):
    # get the srt file name
    file_name = myzipfile.split('\\')[-1:][0].strip(".zip")
    print file_name
    print "unzipping file"
    # create a folder with the name of the file
    if not os.path.exists('temp'):
        os.mkdir('temp')
    extract_dir = 'temp'
    # create the zip object based on zipped file
    zip_ref = zipfile.ZipFile(myzipfile, 'r')
    # extract file into the folder
    zip_ref.extractall(extract_dir)
    zip_ref.close()
    tif = os.path.join(extract_dir, file_name + ".tif")
    
    # compress
    comp_tif = os.path.join('compressed_srtm', file_name + ".tif")
    comp_cmd = ['gdal_translate', '-co', 'COMPRESS=LZW', tif, comp_tif]
    subprocess.check_call(comp_cmd)
   
    # delete uncompressed file
    shutil.rmtree('temp')
unzipfiles(r"U:\sgibbes\workplan_2017\litter\landcover\ftp.glcf.umd.edu\glcf\Global_LNDCVR\UMD_TILES\Version_5.1\2012.01.01\MCD12Q1_V51_LC1.2012.FE1718\MCD12Q1_V51_LC1.2012.FE1718.tif.gz")


