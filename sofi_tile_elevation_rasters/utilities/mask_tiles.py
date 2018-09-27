import util


def mask_tiles(tcd_tile):
    vrt = 'tile.vrt'
    tcd_s3 = 's3://gfw2-data/forest_cover/2000_treecover/{}'
    masked_output = 's3://gfw2-data/alerts-tsv/sofi/raster-analysis/elevation/tif/'

    if len(tcd_tile) != 0 and '.tif' in tcd_tile:
        
        # download tcd tile
        util.download(tcd_s3.format(tcd_tile), 'data/tcd/')

        # clip elevation raster to extent boox
        clipped_elevation = util.clip_raster(vrt, 'data/tcd/{}'.format(tcd_tile))

        # mask to 30% tcd
        masked_30tcd = util.mask_raster(clipped_elevation, 'data/tcd/{}'.format(tcd_tile))

        # upload to s3
        util.upload_to_s3(masked_30tcd, masked_output)

        # clean workspace
        util.clean_workspace(tcd_tile.replace('Hansen_GFC2014_treecover2000_', ''))
