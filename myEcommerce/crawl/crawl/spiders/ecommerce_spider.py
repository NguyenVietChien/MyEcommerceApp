import scrapy
from scrapy.crawler import CrawlerProcess
# from twisted.internet import reactor
from ..items import CrawlItem
from scrapy.utils.project import get_project_settings
from scrapy.spiders import CrawlSpider


class EcommerceSpiderSpider(CrawlSpider):
    name = 'tiki'

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        print(self.url)
        self.domain = kwargs.get('domain')
        self.allowed_domains = [self.domain]

    def start_requests(self):
        yield scrapy.Request(self.url, self.parse)

    def parse(self, response):
        items = CrawlItem()
        # Save div of items from web to scrape
        product = response.css("a.product-item")
        # Save details from item
        for responses in product:
            product_name = responses.css("h3::text").extract()
            product_discount = responses.css(
                ".price-discount__discount::text").getall()
            product_link = "https://tiki.vn" + str(responses.attrib['href'])
            product_price = responses.css(
                ".price-discount__price").css("::text").get()

            rating_point = response.css(".review-rating__point::text").get()
            total_comments = response.css(".review-rating__total::text").get()
            rating_5_star = response.xpath(
                '//*[@id="__next"]/div[1]/main/div[3]/div[4]/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/div[3]/text()').get()
            rating_4_star = response.xpath(
                '//*[@id="__next"]/div[1]/main/div[3]/div[4]/div/div[2]/div[1]/div[1]/div/div[2]/div[2]/div[3]/text()').get()
            rating_3_star = response.xpath(
                '//*[@id="__next"]/div[1]/main/div[3]/div[4]/div/div[2]/div[1]/div[1]/div/div[2]/div[3]/div[3]/text()').get()
            rating_2_star = response.xpath(
                '//*[@id="__next"]/div[1]/main/div[3]/div[4]/div/div[2]/div[1]/div[1]/div/div[2]/div[4]/div[3]/text()').get()
            rating_1_star = response.xpath(
                '//*[@id="__next"]/div[1]/main/div[3]/div[4]/div/div[2]/div[1]/div[1]/div/div[2]/div[5]/div[3]/text()').get()
            # Store data into item.
            items['product_link'] = product_link
            items['product_name'] = product_name
            items['product_price'] = int(product_price.replace(
                "₫", "").replace(".", "").replace(" ", ""))
            items['product_discount'] = product_discount

            items['rating_point'] = rating_point
            items['total_comments'] = total_comments

            items['rating_5_star'] = rating_5_star
            items['rating_4_star'] = rating_4_star
            items['rating_3_star'] = rating_3_star
            items['rating_2_star'] = rating_2_star
            items['rating_1_star'] = rating_1_star
            items['platform'] = 'tiki'

            yield items

        numpage = str(EcommerceSpiderSpider.page_number)
        print(numpage)
        # print(numpage + "------------------------------------------------")
        # next_page = EcommerceSpiderSpider.url + "&page=" + numpage
        # if EcommerceSpiderSpider.page_number < 4:
        #     EcommerceSpiderSpider.page_number += 1
        #     yield response.follow(next_page, callback=self.parse)

# Run Scrapy from a script
