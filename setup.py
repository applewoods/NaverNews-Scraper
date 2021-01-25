from setuptools import setup

setup(
    name = naver_news_scraper_lib,
    version = "1.0.0",
    description = "woo's naver news scrap",
    url = "https://github.com/applewoods/NaverNews-Scraper.git",
    author = "applewoods",
    install_requires = [
        'pandas==1.1.3',
        'beautifulsoup4==4.4.1',
        'requests==2.24.0'
    ]
)