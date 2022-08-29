import scrapy
from scrapy.http import HtmlResponse
from amazonuk.items import AmazonukItem
from scrapy.loader import ItemLoader
import os
import json


class AmazonbooksSpider(scrapy.Spider):
    name = 'amazonbooks'
    allowed_domains = ['amazon.co.uk']
    start_urls = ['https://www.amazon.co.uk/gp/bestsellers/books']

    zyte_smartproxy_enabled = True
    zyte_smartproxy_apikey = '819580e1d3324ab39ca46dafd7cb09df'

    def parse(self, response):
        raw_data = response.css('[data-client-recs-list]::attr(data-client-recs-list)').get()
        data = json.loads(raw_data)
        for item in data:
            url = 'https://www.amazon.co.uk/dp/{}'.format(item['id'])
            yield scrapy.Request(url, callback=self.parse_item, meta={'rank': item['metadataMap']['render.zg.rank'],
                                                                      'id': item['id']})

        next_page = response.css('.a-last a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_item(self, response):
        rank = response.meta.get('rank')
        id = response.meta.get('id')

        book_item = ItemLoader(item=AmazonukItem(), selector=response)
        book_item.add_css('book_title', '.a-size-extra-large')
        book_item.add_css('author','.a-link-normal.contributorNameID')
        book_item.add_value('rank', rank)
        book_item.add_css('price', '.a-size-base.a-color-price.a-color-price')
        book_item.add_css('cover', '.a-dynamic-image.image-stretch-vertical.frontImage::attr(src)')
        book_item.add_value('book_url', response.url)
        book_item.add_value('book_id', id)

        yield book_item.load_item()


