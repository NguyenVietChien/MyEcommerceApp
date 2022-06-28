import scrapy
from ..items import CrawlItem


class ShopeeSpider(scrapy.Spider):
    name = 'shopee'
    page_number = 1
    start_urls = [
        'https://shopee.vn/search?keyword=%C4%91%E1%BB%93%20ch%C6%A1i&trackingId=searchhint-1648921902-8e474d9a-b2ad-11ec-a003-08f1ea7b4e08'
    ]

    def parse(self, response):
        items = CrawlItem()

        # create
        product = response.css(".shopee-search-item-result__item")

        for responses in product:
            product_name = responses.css("._3IqNCf::text").extract()
            product_price = responses.css("._3c5u7X::text").extract()
            product_discount = responses.css(
                "div.percent").css("::text").extract()
            product_link = "https://shopee.vn" + \
                str(responses.css('a::attr(href)').get())

            items['product_link'] = product_link
            items['product_name'] = product_name
            items['product_price'] = product_price
            items['product_discount'] = product_discount
            yield items
        numpage = str(ShopeeSpider.page_number)

        page_total = response.css(
            ".shopee-mini-page-controller__total::text").get()
        print(
            numpage + "------------------------------------------------" + str(page_total))
        next_page = "https://shopee.vn/search?keyword=%C4%91%E1%BB%93%20ch%C6%A1i&page=" + \
            numpage + "&trackingId=searchhint-1648921902-8e474d9a-b2ad-11ec-a003-08f1ea7b4e082"

        # if  len(product.extract()) != 0:
        if ShopeeSpider.page_number < int(page_total)-1:
            ShopeeSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)
