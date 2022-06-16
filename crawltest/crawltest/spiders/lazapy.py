from scrapy_splash import SplashRequest
from ..items import ProductItem
import scrapy


class LazapySpider(scrapy.Spider):
    name = 'lazapy'

    start_urls = ['https://www.lazada.vn/catalog/?spm=a2o4n.searchlistcategory.search.1.6ba2293c2eUvnW&q=%C4%91%E1%BB%93%20ch%C6%A1i&_keyori=ss&from=search_history&sugg=%C4%91%E1%BB%93%20ch%C6%A1i_0_1']
    page_number = 1
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
            
            assert(splash:runjs("document.querySelector('button.shopee-button-outline.shopee-mini-page-controller__next-btn').click()"))
            assert(splash:wait(2))

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
            req = SplashRequest(url,
                                endpoint='render.html',
                                args={'lua_source': self.script3,
                                      'wait': 0.5,
                                      'viewport': '1024x2480',
                                      'timeout': 90,
                                      'images': 0,
                                      },
                                callback=self.parse,

                                )

            req2 = SplashRequest(
                url,
                endpoint="render.html",
                args={
                    'wait': 5,
                },
                callback=self.parse,
                dont_filter=True
            )
            req3 = SplashRequest(
                url=url,
                callback=self.parse,
                meta={
                    "splash": {
                        "endpoint": "render.html",
                        "args": {
                            'wait': 5,
                            'url': url,
                            "lua_source": self.render_script,

                        },
                    }
                },
                dont_filter=True,
            )
            yield req

    def parse(self, response):
        item = ProductItem()
        # print(response.body)
        # print(response.data['html'])
        for data in response.css('.Bm3ON'):
            # print(data)
            # item["price"] = data.css(".ZEgDH9::text").extract_first()
            link = data.css('.RfADt').css('a::attr(href)').get()
            if link is not None:
                link = response.urljoin(link)

            req1 = SplashRequest(
                url=link,
                callback=self.parse_detail,
                meta={
                    "splash": {
                        "endpoint": "render.html",
                        "args": {
                            'wait': 5,
                            'url': link,
                            "lua_source": self.render_script2,
                        },
                    }
                },
                dont_filter=True
            )

            req2 = scrapy.Request(link, callback=self.parse_detail)

            yield req2

        # current_page = response.css(
        #     '.shopee-mini-page-controller__current::text').extract_first()[0]
        total_page = response.xpath(
            '//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[3]/div/ul/li[8]/a/text()').get()

        # print('Page:', current_page, '/', total_page)
        numpage = str(LazapySpider.page_number)
        print(
            numpage + "------------------------------------------------" + str(total_page))

        next_page = "https://www.lazada.vn/catalog/?_keyori=ss&from=search_history&page=" + numpage + \
            "&q=%C4%91%E1%BB%93%20ch%C6%A1i&spm=a2o4n.searchlistcategory.search.1.6ba2293c2eUvnW&sugg=%C4%91%E1%BB%93%20ch%C6%A1i_0_1"

        # if current_page != total_page:
        if LazapySpider.page_number < 13:
            LazapySpider.page_number += 1
            req1 = SplashRequest(
                url=next_page,
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

            req = SplashRequest(next_page,
                                endpoint='render.html',
                                args={'lua_source': self.script3,
                                      'wait': 0.5,
                                      'viewport': '1024x2480',
                                      'timeout': 90,
                                      'images': 0,
                                      },
                                callback=self.parse,
                                dont_filter=True
                                )
            yield req

    def parse_detail(self, response):

        name = response.css(".pdp-mod-product-badge-title").css("::text").get()
        price = response.css(".pdp-price_size_xl").css("::text").get()
        score = response.css(".score-average").css("::text").get()
        yield {
            # 'link': link,
            'name': name,
            'price': price,
            'score': score
        }
