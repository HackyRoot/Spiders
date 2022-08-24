import scrapy
from fragrancedirect.items import  FragrancedirectItem
from scrapy.loader import ItemLoader

class FragrancedirectSpider(scrapy.Spider):
    name = 'fragrance'
    allowed_domains = ['fragrancedirect.co.uk']
    start_urls = ['https://www.fragrancedirect.co.uk/gb/en/brands/abercrombie-fitch']

    def parse(self, response):
        top_navs = response.css('.nav-main a::attr(href)').getall()
        for url in top_navs:
            self.logger.info('URL: ', url)
            yield scrapy.Request(url, callback=self.parse_shelf)

    def parse_shelf(self, response):
        products = response.css('#searchResults .list-item__container')

        if not response.meta.get('pagination'):

            for product in products:
                # l = ItemLoader(item=FragrancedirectItem, selector=product)
                #
                # l.add_css('id', '.list-item::attr(data-object-id)')
                # l.add_css('product_name', '.list-item::attr(data-product-name)')
                # l.add_css('product_url', '.list-item-image a::attr(href)')
                # l.add_css('product_current_price', '.list-item-price::text')
                # l.add_css('product_save', '.list-item-save::text')

                item = FragrancedirectItem()

                item['id'] = product.css('.list-item::attr(data-object-id)').get()
                item['product_name'] = product.css('.list-item::attr(data-product-name)').get()
                item['product_url'] = product.css('.list-item-image a::attr(href)').get()
                item['product_current_price'] = product.css('.list-item-price::text').get()
                item['product_save'] = product.css('.list-item-save::text').re('/d')

                yield item

            total_pages = response.css('a.paging-next::attr(data-total-pages)').get(0)
            for i in range(int(total_pages)):
                next_page_url = f'{response.url}?page={i}'
                yield scrapy.Request(
                    next_page_url,
                    callback=self.parse_shelf,
                    meta={'pagination': True}
                )