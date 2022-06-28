
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import CrawlItem


class TipySpider(CrawlSpider):

    name = 'tikipy'

    def __init__(self, *args, **kwargs):

        super(TipySpider, self).__init__(*args, **kwargs)
        url = kwargs.get('url').encode('utf8')
        self.url = url.decode('utf8')
        print(self.url)
        self.domain = kwargs.get('domain')
        self.allowed_domains = [self.domain]
        self.start_urls = [self.url]

    rules = (
        Rule(
            LinkExtractor(
                restrict_css=['a.product-item', '.WebpImg__StyledImg-sc-h3ozu8-0']), callback='parse_item', follow=False),
        Rule(LinkExtractor(restrict_css='.gNgpAR li a'), follow=True)
    )

    def parse_item(self, response):
        items = CrawlItem()

        image = response.css(
            ".WebpImg__StyledImg-sc-h3ozu8-0::attr(src)").get()

        product_link = response.url
        product_id = product_link[product_link.index("spid=")+5:]

        title = response.css("h1.title::text").extract()
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

        if title is not None:
            items['product_id'] = product_id
            items['product_thumbnail'] = image

            items['product_link'] = product_link
            items['product_name'] = title[0]
            items['product_price'] = convert(product_price)

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
