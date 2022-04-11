from setuptools import setup, find_packages

setup(
    name='euroleague-web-scraper',
    version='0.1',
    author='Domantas Baliukynas',
    author_email='domantas.baliukynas@mif.stud.vu.lt',
    description='Web scraper that fetches EuroLeague season, teams, players ' \
        'and puts them into instances.',
    packages=find_packages()
)