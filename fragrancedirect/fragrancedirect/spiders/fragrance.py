import scrapy
from fragrancedirect.items import FragrancedirectItem
from scrapy.loader import ItemLoader

class FragrancedirectSpider(scrapy.Spider):
    name = 'fragrance'
    allowed_domains = ['fragrancedirect.co.uk']
    start_urls = ['https://www.fragrancedirect.co.uk/gb/en/']

    def parse(self, response):
        top_navs = response.css('.nav-main a::attr(href)').getall()
        for url in top_navs:
            self.logger.info(response.urljoin(url))
            yield scrapy.Request(response.urljoin(url), callback=self.parse_shelf)

    def parse_shelf(self, response):
        products = response.css('#searchResults .list-item__container')

        if not response.meta.get('pagination'):
            for product in products:
                item = FragrancedirectItem()

                item['id'] = product.css('.list-item::attr(data-object-id)').get()
                item['product_name'] = product.css('strong::text').get() + product.css('.list-item a[data-ieb-action="product_click"]::text').getall()[3].strip()
                item['product_url'] = product.css('.list-item-image a::attr(href)').get()
                item['product_current_price'] = product.css('.list-item-price::text').get()
                item['product_save'] = product.css('.list-item-save::text').re('\£\d[^\s]+')
                yield item

            total_pages = response.css('a.paging-next::attr(data-total-pages)').get(0)
            for i in range(int(total_pages)):
                next_page_url = f'{response.url}?page={i}'
                yield scrapy.Request(
                    next_page_url,
                    callback=self.parse_shelf,
                    meta={'pagination': True}
                )
