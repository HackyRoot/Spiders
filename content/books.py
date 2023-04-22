import scrapy


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        # Extract book URLs and follow them
        for book in response.css('.product_pod'):
            product_page = book.css('a::attr(href)').get()
            yield response.follow(product_page, callback=self.parse_book)

        # Extract next page URL and follow it
        next_page = response.css('.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_book(self, response):
        # Extract book information and yield as a dictionary
        yield {
            'title': response.css('.product_page .product_main h1::text').get(),
            'url': response.url,
            'price': response.css('.product_page .price_color::text').get(),
            'cover': response.css('.product_page .item.active img').get(),
        }
