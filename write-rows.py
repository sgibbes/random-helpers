import os
from osgeo import ogr
import argparse

def main():
    parser = argparse.ArgumentParser(description='generates list format of rows in a shapefile field')

    parser.add_argument('--shapefile', '-s', required=True, help='an input shapefile')
    parser.add_argument('--field-name', '-f', required=True, help='field name to iterate on')

    args = parser.parse_args()

    shapefile = args.shapefile
    field_name = args.field_name

    driver = ogr.GetDriverByName('ESRI Shapefile')

    dataSource = driver.Open(shapefile, 0) # 0 means read-only. 1 means writeable.

    # Check to see if shapefile is found.

    python_list = []
    if dataSource is None:
        print 'Could not open %s' % (shapefile)
    else:
        print 'Opened %s' % (shapefile)
        layer = dataSource.GetLayer()
        
        for feature in layer:
            python_list.append(feature.GetField(field_name))
            
        layer.ResetReading()
        with open('rows.txt', 'w') as attribute_text:
            attribute_text.write(str(python_list))
            
        print "wrote rows in {} to rows.txt".format(field_name)
        
if __name__ == "__main__":
    main()