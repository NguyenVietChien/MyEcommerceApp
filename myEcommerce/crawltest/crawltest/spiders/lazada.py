# -*- coding: utf-8 -*-
from urllib.parse import urljoin
import scrapy
from scrapy_splash import SplashRequest, SplashFormRequest
from scrapy_selenium import SeleniumRequest


lua_script = """
function main(splash)
    local num_scrolls = 10
    local scroll_delay = 1.0
    local scroll_to = splash:jsfunc("window.scrollTo")
    local get_body_height = splash:jsfunc(
        "function() {return document.body.scrollHeight;}"
    )
    assert(splash:go(splash.args.url))
    splash:wait(splash.args.wait)
    for _ = 1, num_scrolls do
        scroll_to(0, get_body_height())
        splash:wait(scroll_delay)
    end
    return splash:html()
end
"""


class LazadaSpider(scrapy.Spider):

    name = "lazada"
    allowed_domains = ['lazada.vn']
    start_urls = ["https://www.lazada.vn/dien-thoai-di-dong"]  # + str(i)
#                  for i in range(1, 103)]
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
        driver = response.request.meta['driver']
        number = response.xpath(
            '// *[@id="root"]/div/div[3]/div[1]/div/div[1]/div[3]/div/ul/li[8]/a/text()').get()

        for data in response.xpath('//div[@data-qa-locator="product-item"]'):
            name = data.xpath(
                '//*[@id="root"]/div/div[3]/div[1]/div/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/a/text()').extract_first()
            link = data.css('.RfADt').css('a::attr(href)').get()
            # price = data.css('.ooOxS::text').get()
            # place = data.css(".oa6ri::text").extract_first()
            yield {
                'link': link,
                # 'name': name,

            }

        # count = 0
        # while True:
        #     count += 1
        #     try:
        #         button = driver.find_element_by_xpath(
        #             '//*[@id="root"]/div/div[3]/div[1]/div/div[1]/div[3]/div/ul/li[9]/button')
        #         button.click()
        #         print('Page navigated after click: ' + driver.title)
        #         for data in response.xpath('//div[@data-qa-locator="product-item"]'):
        #             name = data.xpath(
        #                 '//*[@id="root"]/div/div[3]/div[1]/div/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/a/text()').extract_first()
        #             link = data.css('.RfADt').css('a::attr(href)').get()
        #             price = data.css('.ooOxS::text').get()
        #             place = data.css(".oa6ri::text").extract_first()
        #             if link is not None:
        #                 link = response.urljoin(link)
        #                 yield scrapy.Request(link, self.parse_detail)

        #         print("Count-------------------------------------------" + str(count))

        #         # get the data and write it to scrapy items
        #     except:
        #         print(response.request.meta['driver'].title +
        #               "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            # break

        # driver.close()

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
