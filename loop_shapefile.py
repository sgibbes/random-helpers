import arcpy
import os
import argparse

# this creates a new file called country_shape on each iteration of the loop

field = ["ISO"] ## use @Shape if you want to pass geometry to other arc tools

with arcpy.da.SearchCursor(country, field) as cursor:
        for row in cursor:
            iso = row[0]
            where = '"ISO" = ' + "'{}'".format(iso)
            country_selection = "country_selection"
            country_shapefile = os.path.join(datadir, "country_shapefile.shp")
            arcpy.Select_analysis(country, country_shapefile, where)