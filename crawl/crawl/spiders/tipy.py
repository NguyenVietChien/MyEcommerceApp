from lib2to3.pgen2 import driver
from turtle import title
import scrapy
# from selenium import webdriver
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import CrawlItem
# PATH = "C:\Program Files (x86)\chromedriver.exe"
# driver = webdriver.Chrome(PATH)


class TipySpider(CrawlSpider):

    name = 'tikipy'
    start_urls = ['']

    tiki_next = LinkExtractor(restrict_css='.gNgpAR li a')
    tiki_product_detail = LinkExtractor(restrict_css='a.product-item')

    rule_next = Rule(tiki_next, follow=True)
    rule_product_detail = Rule(
        tiki_product_detail, callback='parse_item', follow=False)

    rules = (
        rule_product_detail,
        rule_next
    )

    def parse_item(self, response):
        items = CrawlItem()
        title = response.css("title::text").extract()
        product_price = response.css(
            ".product-price__current-price::text").get()

        product_review_rating_point = response.css(
            ".review-rating__point::text").get()
        product_comments = response.css(".review-rating__total::text").get()
        product_review_rating_5_star = response.xpath(
            '//*[@id="__next"]/div[1]/main/div[3]/div[4]/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/div[3]/text()').get()
        product_review_rating_4_star = response.xpath(
            '//*[@id="__next"]/div[1]/main/div[3]/div[4]/div/div[2]/div[1]/div[1]/div/div[2]/div[2]/div[3]/text()').get()
        product_review_rating_3_star = response.xpath(
            '//*[@id="__next"]/div[1]/main/div[3]/div[4]/div/div[2]/div[1]/div[1]/div/div[2]/div[3]/div[3]/text()').get()
        product_review_rating_2_star = response.xpath(
            '//*[@id="__next"]/div[1]/main/div[3]/div[4]/div/div[2]/div[1]/div[1]/div/div[2]/div[4]/div[3]/text()').get()
        product_review_rating_1_star = response.xpath(
            '//*[@id="__next"]/div[1]/main/div[3]/div[4]/div/div[2]/div[1]/div[1]/div/div[2]/div[5]/div[3]/text()').get()

        # print(title)
        if title is not None:
            items['product_link'] = "https://tiki.vn/search?q=%C4%91%E1%BB%93+ch%C6%A1i"
            items['product_name'] = title[0]
            items['product_price'] = convert(product_price)
            # items['product_discount'] = product_discount

            items['rating_point'] = convert_rating_total(
                product_review_rating_point)
            items['total_comments'] = convert(product_comments)

            items['rating_5_star'] = convert(
                product_review_rating_5_star),
            items['rating_4_star'] = convert(
                product_review_rating_4_star),
            items['rating_3_star'] = convert(
                product_review_rating_3_star),
            items['rating_2_star'] = convert(
                product_review_rating_2_star),
            items['rating_1_star'] = convert(
                product_review_rating_1_star),
            items['platform'] = 'tiki'

            yield items
        else:
            scrapy.Spider.close()


def convert_rating_total(rating):
    if rating is None:
        return 0
    else:
        return float(rating)


def convert(string):
    if string is None:
        return 0
    else:
        new = ''
        for i in string:
            if i.isdigit():
                new += i
        return int(new)
