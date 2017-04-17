import subprocess

def unzip_gz(ingz, id):
    inf = gzip.open(ingz, 'rb')
    outf = open(unzipped, 'wb')
    outf.write(inf.read())
    inf.close()
    outf.close()
    
    # compress file
    compr = ['gdal_translate', '-co', 'COMPRESS=LZW', 'outdir/{}_compr.tif'.format(id)]
    