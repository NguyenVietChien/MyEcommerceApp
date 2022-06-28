# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
# from scrapy_djangoitem import DjangoItem
# from myEcommerce.base.models import *


class CrawlItem(scrapy.Item):
    product_id = scrapy.Field()
    product_name = scrapy.Field()
    product_price = scrapy.Field()
    product_thumbnail = scrapy.Field()
    product_link = scrapy.Field()

    rating_point = scrapy.Field()
    total_comments = scrapy.Field()

    rating_5_star = scrapy.Field()
    rating_4_star = scrapy.Field()
    rating_3_star = scrapy.Field()
    rating_2_star = scrapy.Field()
    rating_1_star = scrapy.Field()

    platform = scrapy.Field()
