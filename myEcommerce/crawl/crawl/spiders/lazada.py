# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


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

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse,
                                endpoint="execute",
                                args={'wait': 0.5, 'viewport': '1024x2480', 'timeout': 90, 'images': 0, 'lua_source': lua_script},)

    def parse(self, response):

        for data in response.xpath('//div[@data-qa-locator="product-item"]'):
            name = data.css("a.RfADt::text").extract_first()
            price = data.css('.ooOxS::text').get()
            image = data.css(".oa6ri::text").extract_first()
            yield {
                'name': name,
                'price': price,
                'image': image
            }
