import scrapy
from whiskeyscraper.items import WhiskeyscraperItem
from scrapy.loader import ItemLoader

class WhiskeyspiderSpider(scrapy.Spider):
    name = 'whiskeyspider'
    allowed_domains = ['whiskyshop.com']
    start_urls = ['https://www.whiskyshop.com/scotch-whisky?item_availability=In+Stock']

    def parse(self, response):
        for products in response.css('.product-item-info'):
            items = ItemLoader(item = WhiskeyscraperItem(), selector=products)

            items.add_css('name', '.product-item-link')
            items.add_css('link', '.product-item-link::attr(href)')
            items.add_css('price', '.price')

            yield items.load_item()


        next_page = response.css('.action.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
