import scrapy
from scrapy_splash import SplashRequest
from ..items import ProductItem


class ShopeeCrawlSpider(scrapy.Spider):
    name = 'shopee_crawl'
    allowed_domains = ['https://shopee.vn']
    start_urls = [
        "https://shopee.vn/search?keyword=%C4%91%E1%BB%93%20ch%C6%A1i"]

    render_script = '''
    function main(splash)
        assert(splash:go(splash.args.url))
        # splash:go(splash.args.url)

  	    splash:set_viewport_full()
        assert(splash:wait(5))
        assert(splash:runjs("document.getElementsByClassName('shopee-mini-page-controller__next-btn')[0].click()"))
        assert(splash:wait(5))
        
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
        for data in response.css(".shopee-search-item-result__item"):
            item["name"] = data.css(".Cve6sh::text").extract_first()
            item["price"] = data.css(".ZEgDH9::text").extract_first()

            yield item

        current_page = response.css(
            '.shopee-mini-page-controller__current::text').extract_first()[0]
        total_page = response.css(
            '.shopee-mini-page-controller__total::text').extract_first()

        print('Page:', current_page, '/', total_page)

        if current_page != total_page:
            yield SplashRequest(
                url=response.url,
                callback=self.parse,
                meta={
                    "splash": {
                        "endpoint": "render.html",
                        "args": {
                            'wait': 5,
                            'url': response.url,
                            "lua_source": self.render_script,
                        },
                    }
                },
                dont_filter=True
            )
