from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from appstorecrawler.items import AppstorecrawlerItem
import urlparse

class MySpider(CrawlSpider):
  name = "appstore"
  allowed_domains = ["play.google.com"]
  start_urls = ["https://play.google.com/store/apps/"]
  rules = [Rule(LinkExtractor(allow=(r'apps/details',),deny=(r'reviewId')),follow=True,callback='parse_link')]
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
        item["Link"] = titles.xpath('/html/head/link[6]/@href').extract()
        item["Item_name"] = titles.xpath('//*[@class="id-app-title"]/text()').extract()
        item["Updated"] = titles.xpath('//*[@itemprop="datePublished"]/text()').extract()
        item["Author"] = titles.xpath('//*[@itemprop="author"]/a[1]/span/text()').extract()
        item["Filesize"] = titles.xpath('//*[@itemprop="fileSize"]/text()').extract()
        item["Downloads"] = titles.xpath('//*[@itemprop="numDownloads"]/text()').extract()
        item["Version"] = titles.xpath('//*[@itemprop="softwareVersion"]/text()').extract()
        item["Compatibility"] = titles.xpath('//*[@itemprop="operatingSystems"]/text()').extract()
        item["Content_rating"] = titles.xpath('//*[@itemprop="contentRating"]/text()').extract()
        item["Author_link"] = titles.xpath('//*[@class="content contains-text-link"]/a[1]/@href').extract()
##        item["Author_link_test"] = titles.select('//*[@class="content contains-text-link"]/a/@href').extract()
        item["Genre"] = titles.xpath('//*[@itemprop="genre"]/text()').extract()
        item["Price"] = titles.xpath('//*[@class="price buy id-track-click id-track-impression"]/jsl/span/text()').extract()
        item["Rating_value"] = titles.xpath('//*[@class="score"]/text()').extract()
        item["Review_number"] = titles.xpath('//*[@class="rating-count"]/text()').extract()
##        item["Description"] = response.xpath('//*[@]/text()').extract()
        item["IAP"] = titles.xpath('//*[@class="inapp-msg"]/text()').extract()
        item["Developer_badge"] = titles.xpath('//*[@class="badge-title"]//text()').extract()
        item["Physical_address"] = titles.xpath('//*[@class="content physical-address"]/text()').extract()
        item["Video_URL"] = titles.xpath('//*[@class="play-action-container"]/@data-video-url').extract()
        item["Developer_ID"] = titles.xpath('//*[@itemprop="author"]/a[1]/@href').extract()
        items.append(item)
      return items
      

