import fiona
from shapely.geometry import shape

footprint = r'U:\sgibbes\liz_mask_loss\tiles.shp'
country = r'U:\sgibbes\liz_mask_loss\country_proj.shp'

# open both input datasets
with fiona.open(footprint, 'r') as grid:
    with fiona.open(country, 'r') as country:
    
        # compare each feature in dataset 1 and 2
        for g in grid:
            tileid = g['properties']['unique_id']
            for i in country:
                # print tile ID if geometry intersects
                if shape(g['geometry']).intersects(shape(i['geometry'])):
                    print "{}: intersects".format(tileid)
                else:
                    print "{}: doesn't intersect".format(tileid)
