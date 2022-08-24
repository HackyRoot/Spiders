import scrapy


class WhiskeyspiderSpider(scrapy.Spider):
    name = 'whiskeyspider'
    allowed_domains = ['whiskyshop.com']
    start_urls = ['https://www.whiskyshop.com/scotch-whisky?item_availability=In+Stock']

    def parse(self, response):
        for product in response.css('.product-item-info'):
            try:
                yield {
                    'name': product.css('.product-item-link::text').get(),
                    'link': product.css('.product-item-link::attr(href)').get(),
                    'price': product.css('.price::text').get().replace('£', ''),
                }
            except:
                yield {
                    'name': product.css('.product-item-link::text').get(),
                    'link': product.css('.product-item-link::attr(href)').get(),
                    'price': 'sold out'
                }

        next_page = response.css('.action.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
