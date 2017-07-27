import argparse 
import utilities
                 
def main():

    # Parse commandline arguments
    parser = argparse.ArgumentParser(description='download tiles')
    parser.add_argument('--tile-id', '-t', required=True)
    parser.add_argument('--tcd', dest='tcd', action='store_true')
    parser.add_argument('--loss', dest='loss', action='store_true')
    parser.add_argument('--area', dest='area', action='store_true')
    parser.add_argument('--biomass', dest='biomass', action='store_true')
    parser.add_argument('--create-mosaic', dest='create_mosaic', action='store_true')
    
    args = parser.parse_args()

    data_type_list = utilities.download_tiles(args)
    
    if args.create_mosaic:
        utilities.make_mosaic(data_type_list)
    
if __name__ == '__main__':
    main()