# -*- coding: utf-8 -*-
from urllib.parse import urljoin
import scrapy
from scrapy_splash import SplashRequest, SplashFormRequest
from scrapy_selenium import SeleniumRequest


class LazadaSpider(scrapy.Spider):

    name = "lazadas"
    allowed_domains = ['lazada.vn']
    start_urls = ["https://www.lazada.vn/dien-thoai-di-dong"]
                
    page_number = 1

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                wait_time=3,
                screenshot=True,
                callback=self.parse,
                dont_filter=True
            )

    def parse(self, response):
        number = response.xpath(
            '// *[@id="root"]/div/div[3]/div[1]/div/div[1]/div[3]/div/ul/li[8]/a/text()').get()

        for data in response.xpath('//div[@data-qa-locator="product-item"]'):
            name = data.xpath(
                '//*[@id="root"]/div/div[3]/div[1]/div/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/a/text()').extract_first()
            link = data.css('.RfADt').css('a::attr(href)').get()
            price = data.css('.ooOxS::text').get()
            place = data.css(".oa6ri::text").extract_first()
            if link is not None:
                link = response.urljoin(link)
                yield SeleniumRequest(
                    url=link,
                    wait_time=3,
                    screenshot=True,
                    callback=self.parse_detail,
                    dont_filter=True
                )

        next_page = "https://www.lazada.vn/dien-thoai-di-dong/?page=" + \
            str(LazadaSpider.page_number)
        if LazadaSpider.page_number < 120:
            LazadaSpider.page_number += 1
            yield SeleniumRequest(
                url=next_page,
                wait_time=3,
                screenshot=True,
                callback=self.parse,
                dont_filter=True
            )

    def parse_detail(self, response, **kwargs):
        name = response.css(".pdp-mod-product-badge-title").css("::text").get()
        price = response.css(".pdp-price_size_xl").css("::text").get()
        score = response.css(".score-average").css("::text").get()
        yield {
            # 'link': link,
            'name': name,
            'price': price,
            'score': score
        }
