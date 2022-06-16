from urllib.parse import urljoin
from zoneinfo import available_timezones
from requests import request
import scrapy
from scrapy_splash import SplashRequest
from ..items import ProductItem
from bs4 import BeautifulSoup
from bs4 import SoupStrainer


class ShopeeCrawlSpider(scrapy.Spider):
    name = 'shopee_crawl2'
    # allowed_domains = ['https://shopee.vn']
    start_urls = [
        "https://shopee.vn/search?keyword=%C4%91%E1%BB%93%20ch%C6%A1i"]
    page_number = 1

    item = ProductItem()

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
        splash:set_viewport_full()
        assert(splash:wait(2))
        assert(splash:runjs("document.querySelector('button.shopee-button-outline.shopee-mini-page-controller__next-btn').click()"))
        assert(splash:wait(2))
        
        return {
            html = splash:html(),
            url = splash:url(),
            png=splash:png()
        }
    end
    '''

    render_script2 = """
        function main(splash)
            local url = splash.args.url
            assert(splash:go(url))
            assert(splash:wait(5))

            return {
                html = splash:html(),
                url = splash:url(),
            }
        end
        """

    script3 = """
            function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(0.5))
            return {
                html = splash:html(),
                url = splash:url()
            }
            end
            """

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url,
                endpoint="render.html",
                args={
                    'wait': 0.5,
                    'viewport': '1024x2480',
                    'timeout': 90,
                    'images': 0,
                },
                callback=self.parse,
                dont_filter=True
            )

    def parse(self, response):
        item = ProductItem()
        for data in response.css(".shopee-search-item-result__item"):
            item["location"] = data.css("div.zGGwiV").extract_first()
            item["name"] = data.css(".Cve6sh::text").extract_first()

            link = data.css('a::attr(href)').get()

            if link is not None:
                link = response.urljoin(link)
                item["link"] = link

            request = SplashRequest(
                url=link,
                callback=self.parse_detail,
                cb_kwargs=dict(item=item),
                meta={
                    "splash": {
                        "endpoint": "render.html",
                        "args": {
                            'wait': 0.5,
                            'url': link,
                            "lua_source": self.script3,
                            'viewport': '1024x2480',
                            'timeout': 90,
                            'images': 0,
                        },
                    }
                },
                dont_filter=True
            )

            req = SplashRequest(url=link,
                                callback=self.parse_detail,
                                cb_kwargs=dict(item=item),
                                endpoint='render.html',
                                args={'lua_source': self.script3,
                                      'wait': 0.5,
                                      'viewport': '1024x2480',
                                      'timeout': 90,
                                      'images': 0,
                                      }
                                )

            yield request

        # current_page = response.css('.shopee-mini-page-controller__current::text').extract_first()[0]
        total_page = response.css(
            '.shopee-mini-page-controller__total::text').extract_first()

        # print('Page:', current_page, '/', total_page)
        numpage = str(ShopeeCrawlSpider.page_number)
        print(
            numpage + "------------------------------------------------" + str(total_page))

        next_page = "https://shopee.vn/search?keyword=%C4%91%E1%BB%93%20ch%C6%A1i&page=" + \
            numpage + "&trackingId=searchhint-1648921902-8e474d9a-b2ad-11ec-a003-08f1ea7b4e082"

        # if current_page != total_page:
        # if ShopeeCrawlSpider.page_number < 2:
        #     ShopeeCrawlSpider.page_number += 1
        #     yield SplashRequest(
        #         url=next_page,
        #         callback=self.parse,
        #         meta={
        #             "splash": {
        #                 "endpoint": "execute",
        #                 "args": {
        #                     'wait': 5,
        #                     'url': response.url,
        #                     "lua_source": self.render_script,
        #                 },
        #             }
        #         },
        #         dont_filter=True
        #     )

    def parse_detail(self, response, item):

        # print(response)
        print("_______________________________________________________________________________________________")

        # print(item)
        rating = response.xpath(
            '//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[3]/div[3]/div[1]/div[2]/div/div[2]/div[1]/div[1]/span[1]').get()
        # Product details | status: Done
        product = response.xpath(
            '//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[2]/div[3]/div')
        name3 = product.xpath(
            '//*[@id= "main"]/div/div[2]/div[1]/div/div[2]/div/div[2]/div[3]/div/div[1]/span/text()').get()
        vote = product.xpath(
            '//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div[2]/div[1]').css("::text").get()
        discount = product.xpath(
            '//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[2]/div[3]/div/div[3]/div/div/div/div/div[2]/div[2]').css("::text").get()
        sold = product.xpath(
            '//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div[3]/div[1]').css("::text").get()
        price = product.xpath(
            '//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[2]/div[3]/div/div[3]/div/div/div/div/div/div').css("::text").get()
        old_price = product.xpath(
            '//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[2]/div[3]/div/div[3]/div/div/div/div/div[1]').css("::text").get()

        available_product = product.xpath(
            '//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[2]/div[3]/div/div[4]/div/div[4]/div/div/div[2]/div[2]').css("::text").get()

        ratings = response.xpath(
            '//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div[2]/div[4]/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/span[1]').get()
        # Rating and Comment | Status: Undone
        comment = response.xpath(
            '//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[3]/div[2]')
        comment2 = comment.xpath(
            '//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[3]/div[2]/div[1]/div[2]')
        comment3 = comment2.xpath(
            '//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[3]/div[2]/div[1]/div[2]/div')
        # comment4 = response.css('//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[3]/div[2]/div[1]/div[2]')

        test = response.xpath('//div[@class="page-product__content--left"]')
        test2 = test.xpath(
            '//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[3]/div[3]/div[1]/div[2]').get()
        comment5 = response.xpath('//div[@class="product-ratings"]').get()
        cds = product.xpath(
            '//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div[1]/div[1]').get()
        location = response.xpath(
            '//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[4]/div[2]/div[1]/div[1]/div[1]/div[2]/div[3]/div').get()

        # Shop details | Status: Done
        _shop = response.xpath(
            '//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[3]/div[1]')
        shop_detail = _shop.xpath(
            '//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[3]/div[1]/div[2]')
        shop_rating = shop_detail.xpath(
            '//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[3]/div[1]/div[2]/div[1]/button/span').css("::text").get()
        shop_item = shop_detail.css(".g54jiy::text").getall()
        shop_followers = shop_detail.xpath(
            '//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[3]/div[1]/div[2]/div[3]/div[2]/span').css("::text").get()
        shop = _shop.xpath(
            '//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[3]/div[1]/div[1]/div/div[1]').css("::text").get()

        yield{
            # 'price': price,
            'result 1': comment3.get(),
            # 'result 2': convert(shop_item)
        }


def convert(string):
    if string is None:
        return 0
    # if string.isalnum():

    else:
        new = ''
        for i in string:
            if i.isdigit():
                new += i
            elif i == 'k':
                new += "00"
        return int(new)
