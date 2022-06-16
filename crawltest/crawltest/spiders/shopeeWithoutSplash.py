import scrapy
from scrapy_splash import SplashRequest
from ..items import ProductItem

class ShopeeCrawlSpider(scrapy.Spider):
    name = 'shope'
    allowed_domains = ['https://shopee.vn']
    start_urls = ["https://shopee.vn/search?keyword=%C4%91%E1%BB%93%20ch%C6%A1i"]

    

    def parse(self, response):
        item = ProductItem()
        for data in response.css(".shopee-search-item-result__item"):
            item["name"] = data.css(".Cve6sh::text").extract_first()
            item["price"] = data.css(".ZEgDH9::text").extract_first()
            
            yield item
