import scrapy
from scrapy_splash import SplashRequest
from ..items import ProductItem


class ShopeeCrawlSpider(scrapy.Spider):
    name = 'shopees'
    allowed_domains = ['https://shopee.vn']
    start_urls = ["https://shopee.vn/sp.btw2"]

    render_script = '''
    function main(splash)
        assert(splash:go(splash.args.url))
        assert(splash:wait(2))

        local num_scrolls = 10
        local scroll_delay = 1

        local scroll_to = splash:jsfunc("window.scrollTo")
        local get_body_height = splash:jsfunc(
            "function() {return document.body.scrollHeight;}"
        )

        for _ = 1, num_scrolls do
            local height = get_body_height()
            for i = 1, 10 do
                scroll_to(0, height * i/10)
                splash:wait(scroll_delay/10)
            end
        end

        assert(splash:wait(2))
        assert(splash:runjs("document.querySelector('button.shopee-icon-button.shopee-icon-button--right').click()"))
        assert(splash:wait(2))
        
        return {
            html = splash:html(),
            url = splash:url(),
        }
    end
    '''

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url,
                endpoint="render.html",
                args={
                    'wait': 5,
                },
                callback=self.parse,
                dont_filter=True
            )

    def parse(self, response):
        item = ProductItem()
        for data in response.css("div.shop-search-result-view__item"):
            item["name"] = data.css("div._2mQnW2::text").extract_first()

            sale = data.css("div.WTFwws._3f05Zc._3_-SiN")
            if sale:
                item["price"] = data.css(
                    "div.WTFwws._3f05Zc._3_-SiN ::text").extract_first().lstrip('₫')
                # item["price_sale"] = data.css("div.WTFwws._1lK1eK._5W0f35 span:last-child ::text").extract_first()
            else:
                item["price"] = data.css(
                    "div.WTFwws._1lK1eK._5W0f35 > span._29R_un:last-child ::text").extract_first()
                # item["price_sale"] = 'No discount'

            sold = data.css("div.go5yPW ::text").extract_first()
            item["sold"] = sold.split()[2] if sold else 0

            yield item

        current_page = response.css(
            '.shopee-mini-page-controller__current').getall()
        total_page = response.css(
            '.shopee-mini-page-controller__total').getall()
        print('Page:', current_page, '/', total_page)

        if current_page != total_page:
            yield SplashRequest(
                url=response.url,
                callback=self.parse,
                meta={
                    "splash": {
                        "endpoint": "execute",
                        "args": {
                            'wait': 5,
                            'url': response.url,
                            "lua_source": self.render_script,
                        },
                    }
                },
                dont_filter=True
            )
