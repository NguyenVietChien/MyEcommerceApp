from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor
from crawl.crawl.spiders.tipy import TipySpider
from crawl.spiders.ecommerce_spider import EcommerceSpiderSpider
from crawl.spiders.shopee import ShopeeSpider
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerRunner

configure_logging()
settings = get_project_settings()
runner = CrawlerRunner(settings)
runner.crawl(EcommerceSpiderSpider)
runner.crawl(TipySpider)
d = runner.join()
d.addBoth(lambda _: reactor.stop())

reactor.run()
