# -*- coding: utf-8 -*-

# Scrapy settings for gplaycrawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'appstorecrawler'

SPIDER_MODULES = ['appstorecrawler.spiders']
NEWSPIDER_MODULE = 'appstorecrawler.spiders'
CONCURRENT_REQUESTS_PER_DOMAIN = 100
#ITEM_PIPELINES = ['appstorecrawler.pipelines.AppstorecrawlerPipeline']

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Alo Ventures (+http://alo.ventures)'

REACTOR_THREADPOOL_MAXSIZE = 20
LOG_LEVEL = 'INFO'
COOKIES_ENABLED = False
##RETRY_ENABLED = False
DOWNLOAD_TIMEOUT = 60
##REDIRECT_ENABLED = False
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1

ITEM_PIPELINES = {'appstorecrawler.pipelines.AppstorecrawlerPipeline':300 }

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "applestore"
MONGODB_COLLECTION = "metadata"

#DOWNLOAD_DELAY = 0.5

DOWNLOADER_MIDDLEWARES = {
    'scrapyproduct.middlewares.ProxyMiddleware': 1,
    'scrapyproduct.middlewares.DelayAfterConnectionRefusedMiddleware': 510,
}
