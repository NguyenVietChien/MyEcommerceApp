# -*- coding: utf-8 -*-
from os import link
import re

import scrapy

from .. import items


class CrawlerSpider(scrapy.Spider):
    name = 'crawler'

    start_urls = [
        "https://www.inven.co.kr/board/maple/2587?p=&fbclid=IwAR1wKnNeqOhVI0pLhEDLT0JQzOpOhKPh2GGpZDb0nnQeREneCsOGPMgAIWM"
    ]

    def start_requests(self):
        # for i in range(1, 2):  # 페이지 하나씩 넘어가기
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):  # Nhận tất cả các bài đăng trên một trang
        board = response.xpath('//*[@id="new-board"]/form/div')

        for elem in board:
            # Truy cập vào href của bài đăng trên mỗi trang và nhận tiêu đề, nội dung, số lượng đề xuất và lượt xem
            link = elem.xpath(
                '//*[@id="new-board"]/form/div/table/tbody/tr[4]/td[2]/div/div/a/@href').get()
            yield scrapy.Request(link, self.parse_post)

    def parse_post(self, response):
        # item = items.ScrapyAppItem()
        title = response.xpath(
            '//*[@id="tbArticle"]/div[3]/div[1]/div[1]').get()

        yield {
            'title': title
        }
