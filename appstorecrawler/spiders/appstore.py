from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from appstorecrawler.items import AppstorecrawlerItem
import urlparse

class MySpider(CrawlSpider):
  name = "appstore"
  allowed_domains = ["itunes.apple.com"]
  start_urls = ["https://www.apple.com/itunes/charts/"]
  rules = [Rule(LinkExtractor(allow=(r'/us/app/',)),follow=True,callback='parse_link')]
    	# r'page/\d+' : regular expression for http://isbullsh.it/page/X URLs
    	#Rule(LinkExtractor(allow=(r'apps')),follow=True,callback='parse_link')]
    	# r'\d{4}/\d{2}/\w+' : regular expression for http://isbullsh.it/YYYY/MM/title URLs
  def abs_url(url, response):
      """Return absolute link"""
      base = response.xpath('//head/base/@href').extract()
      if base:
        base = base[0]
      else:
        base = response.url
      return urlparse.urljoin(base, url)
    
  def parse_link(self,response):
      hxs = Selector(response)
      titles = hxs.xpath('/html')
      items = []
      for titles in titles :
        item = AppstorecrawlerItem()
        item["Link"] = titles.xpath('//*[@rel="canonical"]/@href').extract()
        item["Item_name"] = titles.xpath('//h1[@itemprop="name"]/text()').extract()
        item["Updated"] = titles.xpath('//*[@itemprop="datePublished"]/text()').extract()
        item["Author"] = titles.xpath('//span[@itemprop="name"]/text()').extract()
        item["Filesize"] = titles.xpath('//ul[@class="list"]/li[5]/text()').extract()
##        item["Downloads"] = titles.xpath('//*[@itemprop="numDownloads"]/text()').extract()
        item["Version"] = titles.xpath('//*[@itemprop="softwareVersion"]/text()').extract()
        item["Compatibility"] = titles.xpath('//*[@itemprop="operatingSystem"]/text()').extract()
        item["Content_rating"] = titles.xpath('//*[@class="app-rating"]/a/text()').extract()
        item["Author_link"] = titles.xpath('//*[@class="app-links"]/a[1]/@href').extract()
##        item["Author_link_test"] = titles.select('//*[@class="content contains-text-link"]/a/@href').extract()
        item["Genre"] = titles.xpath('//*[@itemprop="applicationCategory"]/text()').extract()
        item["Price"] = titles.xpath('//*[@itemprop="price"]/text()').extract()
        item["Rating_value"] = titles.xpath('//*[@itemprop="ratingValue"]/text()').extract()
        item["Rating_count"] = titles.xpath('//*[@itemprop="reviewCount"]/text()').extract()
        item["Description"] = response.xpath('//*[@itemprop="description"]/text()').extract()
        item["Language"] = response.xpath('//*[@class="language"]/text()').extract()
##        item["IAP"] = titles.xpath('//*[@class="inapp-msg"]/text()').extract()
##        item["Developer_badge"] = titles.xpath('//*[@class="badge-title"]//text()').extract()
##        item["Physical_address"] = titles.xpath('//*[@class="content physical-address"]/text()').extract()
##        item["Video_URL"] = titles.xpath('//*[@class="play-action-container"]/@data-video-url').extract()
##        item["Developer_ID"] = titles.xpath('//*[@itemprop="author"]/a[1]/@href').extract()
        items.append(item)
      return items
      

