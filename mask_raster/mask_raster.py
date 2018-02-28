import multiprocessing
import main

tile_list = ['10N_000E']

if __name__ == '__main__':
    count = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=count-2)
    pool.map(main.mask_raster, tile_list)
