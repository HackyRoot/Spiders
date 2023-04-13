from scrapy import Spider, Request
import json


class BooksToScrapeComSpider(Spider):

    name = "amazon_books_scrape"
    start_urls = [
        "https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_nav_0"
    ]

    def parse(self, response):
        raw_data = response.css('[data-client-recs-list]::attr(data-client-recs-list)').get()
        data = json.loads(raw_data)

        for item in data:
            url = 'https://www.amazon.co.in/dp/{}'.format(item['id'])
            yield Request(url, callback=self.parse_item, meta={'rank': item['metadataMap']['render.zg.rank'],
                                                                      'id': item['id']})

        next_page = response.css('.a-last a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_item(self, response):
        rank = response.meta.get('rank')
        id = response.meta.get('id')
        authors = response.css(
            '#bylineInfo_feature_div #bylineInfo span.author.notFaded a.a-link-normal::text').getall()[2:]

        yield{
            "book_url": response.url,
            'author': authors,
            'rank': rank,
            'id': id,
            'book_title': response.css('.a-size-extra-large::text').get(),
            'price': response.css('.a-color-price::text').get(),
            'cover': response.css('.frontImage::attr(src)').get()
        }

