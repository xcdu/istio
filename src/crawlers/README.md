# Crawler
[![Scrapy](https://img.shields.io/badge/Scrapy-2.4.1-blue)](https://docs.scrapy.org/en/latest/)
[![scrapy-splash](https://img.shields.io/badge/scrapy--splash-0.7.2-blue)](https://docs.scrapy.org/en/latest/)

Crawlers are used to gathering corpora to reinforce the feature engineering of NLP module.

## Usage

We use Scrapy framework and scrapy-splash plugin to crawl necessary data.
Please check the official documents ([Scrapy](https://docs.scrapy.org/en/latest/) and [scrapy-splash](https://github.com/scrapy-plugins/scrapy-splash)) to install them:

Before starting the crawling, you need to boot the scrapy-splash docker first:

```shell
docker run -it -p 8050:8050 --rm scrapinghub/splash
```
