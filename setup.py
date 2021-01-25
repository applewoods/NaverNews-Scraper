import naver_news_scraper_lib
from setuptools import setup

setup(
    name = naver_news_scraper_lib,
    version = "1.0.0",
    description = "woo's naver news scrap",
    url = "https://github.com/applewoods/NaverNews-Scraper.git",
    author = "applewoods",
    install_requires = [
        'pandas',
        'bs4',
        'requests',
        'datetime'
    ]
)