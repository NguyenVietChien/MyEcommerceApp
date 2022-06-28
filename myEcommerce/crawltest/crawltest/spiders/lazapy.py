from scrapy_splash import SplashRequest
from ..items import CrawlItem, ProductItem
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
            assert(splash:wait(0.5))
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
        item = CrawlItem()
        for data in response.css('.Bm3ON'):

            img = data.css('.picture-wrapper').css('img').xpath('@src').get()
            # item["product_img"] = img

            link = data.css('.RfADt').css('a::attr(href)').get()
            if link is not None:
                link = response.urljoin(link)
            item["product_link"] = link
            item["platform"] = 'lazada'
            item["product_id"] = link[link.index("-i")+2:link.index(".html")]

            req1 = SplashRequest(
                url=link,
                cb_kwargs=dict(item=item),
                callback=self.parse_detail,
                meta={
                    "splash": {
                        "endpoint": "render.html",
                        "args": {
                            'wait': 0.5,
                            # 'url': link,
                            "lua_source": self.render_script,
                            'viewport': '1024x2480',
                            'timeout': 90,
                            'images': 0,
                        },
                    }
                },
                dont_filter=True
            )
            yield req1

        total_page = response.xpath(
            '//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[3]/div/ul/li[8]/a/text()').get()

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

    def parse_detail(self, response, item):

        name = response.css(".pdp-mod-product-badge-title").css("::text").get()
        item['product_name'] = name

        price = response.css(".pdp-price_size_xl").css("::text").get()
        item['product_price'] = convert(price)

        rating_point = response.css(".score-average").css("::text").get()
        item['rating_point'] = convert_rating_total(rating_point)

        total_comments = response.css(".count").css("::text").get()
        item['total_comments'] = convert(total_comments)

        _5star_xpath = '//*[@id="module_product_review"]/div/div/div[1]/div[2]/div/div/div[2]/ul/li[1]/span[2]'
        rating_5_star = response.xpath(_5star_xpath).css("::text").get()
        item['rating_5_star'] = convert(rating_5_star)

        _4star_xpath = '//*[@id="module_product_review"]/div/div/div[1]/div[2]/div/div/div[2]/ul/li[2]/span[2]'
        rating_4_star = response.xpath(_4star_xpath).css("::text").get()
        item['rating_4_star'] = convert(rating_4_star)

        _3star_xpath = '//*[@id="module_product_review"]/div/div/div[1]/div[2]/div/div/div[2]/ul/li[3]/span[2]'
        rating_3_star = response.xpath(_3star_xpath).css("::text").get()
        item['rating_3_star'] = convert(rating_3_star)

        _2star_xpath = '//*[@id="module_product_review"]/div/div/div[1]/div[2]/div/div/div[2]/ul/li[4]/span[2]'
        rating_2_star = response.xpath(_2star_xpath).css("::text").get()
        item['rating_2_star'] = convert(rating_2_star)

        _1star_xpath = '//*[@id="module_product_review"]/div/div/div[1]/div[2]/div/div/div[2]/ul/li[5]/span[2]'
        rating_1_star = response.xpath(_1star_xpath).css("::text").get()
        item['rating_1_star'] = convert(rating_1_star)

        yield item


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
