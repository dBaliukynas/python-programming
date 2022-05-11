#!/usr/bin/env python3

import time

from scraper import scraper
from instance_utils import file_operations as fo


def main():
    start_scraper_time = time.perf_counter()

    # season_scraper = scraper.EuroLeagueScraper(
    #     team_verbose=True, threading=False)
    # season_without_threading = season_scraper.create_season()

    finish_scraper_time = time.perf_counter()
    total_scraper_time = finish_scraper_time-start_scraper_time

    print(f'Total time: {total_scraper_time} seconds\n')

    start_scraper_threading_time = time.perf_counter()

    season_scraper_threading = scraper.EuroLeagueScraper(
        team_verbose=True, player_verbose=False)
    season_with_threading = season_scraper_threading.create_season()

    finish_scraper_threading_time = time.perf_counter()
    total_scraper_threading_time = finish_scraper_threading_time - \
        start_scraper_threading_time

    print(
        f'Total time: {total_scraper_threading_time} seconds\n')
    print('------------------------------------------------------------------------')

    print(f'Scraper time without thread pool: {total_scraper_time} seconds')
    print(
        f'Scraper time with thread pool: {total_scraper_threading_time} seconds')

    print(
        f'Time difference: {total_scraper_time - total_scraper_threading_time} seconds\n')
    print(
        f'Scraper with thread pool is faster {total_scraper_time / total_scraper_threading_time} times\n')
    print(
        f'Total player creation fails: {scraper.EuroLeagueScraper.player_creation_fails}')
    print(
        f'Total team creation fails: {scraper.EuroLeagueScraper.team_creation_fails}')

    print('------------------------------------------------------------------------\n')

    fo.write_to_file([[season_with_threading]],
                     '../data/season.json')

    # season = fo.convert_to_instances(fo.load_from_file(
    #     '../data/testing1.json', '../data/testing2.json'), vars(scraper))


if __name__ == '__main__':
    main()
