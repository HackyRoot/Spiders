import scrapy


class FragrancedirectSpider(scrapy.Spider):
    name = 'fragrance'
    allowed_domains = ['fragrancedirect.co.uk']
    start_urls = ['https://www.fragrancedirect.co.uk/']

    def parse(self, response):
        top_navs = response.css('.nav-main a::attr(href)').getall()
        for url in top_navs:
            print('--------------------URL------------------', url)
            yield scrapy.Request(url, callback=self.parse_shelf)

    def parse_shelf(self, response):
        products = response.css('#searchResults .list-item__container')
        for product in products[:5]:
            yield {
                'id': product.css('.list-item::attr(data-object-id)').get(),
                'product_name': product.css('.list-item::attr(data-product-name)').get(),
                'product_url': product.css('.list-item-image a::attr(href)').get(),
                'product_current_price': product.css('.list-item-price::text').get(),
                'product_save': product.css('.list-item-save::text').get(),
                'product_rating': product.css('.bv-off-screen::text').get(),
            }

        if not response.meta.get('pagination'):
            total_pages = response.css('a.paging-next::attr(data-total-pages)').get(0)
            for i in range(int(total_pages)):
                next_page_url = f'{response.url}?page={i}'
                yield scrapy.Request(
                    next_page_url,
                    callback=self.parse_shelf,
                    meta={'pagination': True}
                )