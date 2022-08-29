import scrapy
from scrapy.http import HtmlResponse
from amazonuk.items import AmazonukItem
from scrapy.loader import ItemLoader
import os


class AmazonbooksSpider(scrapy.Spider):
    name = 'amazonbooks'
    allowed_domains = ['amazon.co.uk']
    start_urls = ['https://www.amazon.co.uk/gp/bestsellers/books']

    zyte_smartproxy_enabled = True
    zyte_smartproxy_apikey = '819580e1d3324ab39ca46dafd7cb09df'

    def parse(self, response):
        books = response.css('.a-column.a-span12.a-text-center._cDEzb_grid-column_2hIsc')

        for book in books:
            book_item = ItemLoader(item=AmazonukItem(), selector=book)

            book_item.add_css('rank', '.zg-bdg-text')
            book_item.add_css('book_title', '._cDEzb_p13n-sc-css-line-clamp-1_1Fn1y')
            book_item.add_css('author', '.a-size-small.a-link-child ._cDEzb_p13n-sc-css-line-clamp-1_1Fn1y'),

            yield book_item.load_item()

            domain = response.url
            next_page = response.css('.a-last a::attr(href)').get()
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)
