import subprocess

def mask_high_carbon(tileid):

    tcd_tif = 'Hansen_GFC2014_treecover2000_{}.tif'
    highcarbon_tif = '{}_carbon.tif'

    tcd_tile = 's3://gfw2-data/forest_cover/2000_treecover/{}'.format(tcd_tif)
    high_carbon_tile = 's3://gfw-files/sam/carbon_budget/carbon_011018/carbon/{}'.format(highcarbon_tif)

    #copy down tcd tile
    for source in [tcd_tile, high_carbon_tile]:
        print 'downloading {}'.format(source.format(tileid))
        copy_cmd = ['aws', 's3', 'cp', source.format(tileid), '.']

        subprocess.check_call(copy_cmd)

    #mask tcd by 30 and high carbon
    calc = '(A>30) * B'
    highcarbon_30tcd = highcarbon_tif.replace('.tif', '_30tcd.tif')

    outfile = '--outfile={}'.format(highcarbon_30tcd)

    cmd = ['gdal_calc.py', '-A', tcd_tif.format(tileid), '-B', highcarbon_tif.format(tileid), '--cal={}'.format(calc)]
    cmd += ['NoDataValue=255', '--co', 'COMPRESS=LZW', '--outfile={}'.format(highcarbon_30tcd)]

    print "calculating..."
    subprocess.check_call(cmd)
    print "done!"

    #upload to s3
    cmd = ['aws', 's3', 'cp', highcarbon_30tcd, 's3://gfw-files/sam/carbon_budget/carbon_011018/30tcd/carbon/tif/']
    subprocess.check_call(cmd)
