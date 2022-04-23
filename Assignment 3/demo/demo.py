#!/usr/bin/env python3

import time

from scraper import scraper
from scraper import scraper_threading
from instance_utils import file_operations as fo


def main():
    start_scraper_time = time.perf_counter()

    season_scraper = scraper.main()

    finish_scraper_time = time.perf_counter()
    total_scraper_time = finish_scraper_time-start_scraper_time

    print(f'Total time: {total_scraper_time} seconds')

    start_scraper_threading_time = time.perf_counter()

    season_scraper_threading = scraper_threading.main()

    finish_scraper_threading_time = time.perf_counter()
    total_scraper_threading_time = finish_scraper_threading_time - \
        start_scraper_threading_time

    print(
        f'Total time: {total_scraper_threading_time} seconds\n')
    print('------------------------------------------------------------------------')

    print(f'Scraper time without thread pools: {total_scraper_time}\n')
    print(f'Scraper time with thread pools: {total_scraper_threading_time}')

    print(
        f'Time difference: {total_scraper_time - total_scraper_threading_time} seconds\n')
    print(
        f'Scraper with thread pools is faster {total_scraper_time / total_scraper_threading_time} times')

    fo.write_to_file([season_scraper, season_scraper_threading],
                     '../data/testing1.json', '../data/testing2.json', separate=True)
                     
    season = fo.convert_to_instances(fo.load_from_file('../data/testing1.json'), vars(scraper))

if __name__ == '__main__':
    main()
