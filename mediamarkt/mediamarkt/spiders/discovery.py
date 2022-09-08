import scrapy
import re
import json, jmespath
from mediamarkt.items import MediamarktItem
from scrapy.loader import ItemLoader

class DiscoverySpider(scrapy.Spider):
    name = 'discovery'
    allowed_domains = ['mediamarkt.de']
    start_urls = ['https://mediamarkt.de/']

    zyte_smartproxy_enabled = False
    zyte_smartproxy_apikey = '819580e1d3324ab39ca46dafd7cb09df'

    def start_requests(self):
        yield scrapy.Request(
            url="https://mediamarkt.de/",
            callback=self.parse,
            meta={
                "zyte_api": {
                    "browserHtml": True,
                }
            },
        )

    def parse(self, response):
        raw_preloaded_state = response.css('script:contains("__PRELOADED_STATE__")::text').get()
        preloaded_state = re.search('window\.__PRELOADED_STATE__ = (.*?});', raw_preloaded_state).group(1)
        preloaded_state_json = json.loads(preloaded_state)
        sidebar_categories = preloaded_state_json['apolloState']['ROOT_QUERY']['pwaHeader']['categoryNavItems']

        for category_no in range(len(sidebar_categories)):
            if len(sidebar_categories[category_no]['subCategories']) is not 0:
                subCategories = sidebar_categories[category_no]['subCategories']
                for category in subCategories:
                    for product_category in category[0]:
                        product_category_url = product_category['url']
                        yield scrapy.Request(url=response.urljoin(product_category_url),
                                             callback=self.parse_shelf,
                                             meta={
                                                 "zyte_api": {
                                                     "browserHtml": True,
                                                 }
                                             })


            else:
                pass
                # url = sidebar_categories[category_no]['url']
                # yield scrapy.Request(response.urljoin(url), callback=self.parse_shelf)


    def parse_shelf(self, response):
        raw_preloaded_state = response.css('script:contains("__PRELOADED_STATE__")::text').get()
        preloaded_state = re.search('window\.__PRELOADED_STATE__ = (.*?});', raw_preloaded_state).group(1)
        preloaded_state_json = json.loads(preloaded_state)

        product_data = jmespath.search('apolloState', preloaded_state_json)

        product_ids = []

        for product_data_key in list(product_data.keys()):
            if product_data_key.startswith('GraphqlProduct'):
                product_ids.append(product_data_key.split(":")[1])
                print(product_data_key.split(":")[1])

        product_item = ItemLoader(item=MediamarktItem(), selector=product_data)

        for product in product_ids:
            product_id = product_data['GraphqlProduct:' + product]['id']
            product_name = product_data['GraphqlProduct:' + product]['title']
            product_price = product_data['GraphqlPrice:' + product]['productId']
            product_url = product_data['GraphqlProduct:' + product]['url']

            product_item.add_value('product_name', product_name)
            product_item.add_value('product_url', product_url)
            product_item.add_value('product_id', product_id)
            product_item.add_value('product_price', product_price)

            yield product_item.load_item()

        # next_page_url = response.css('')
        # yield scrapy.Request(
        #     next_page_url,
        #     callback=self.parse_shelf)





        # product_categories = preloaded_state_json['apolloState']['ROOT_QUERY']['pwaHeader']['categoryNavItems'][0]['subCategories'][0]

        # for product_category in product_categories[0][0]['url']:

        print(response.raw_api_response)
        # print response.raw_api_response.browserHtml.css('h1')
        # {
        #     'url': 'https://quotes.toscrape.com/',
        #     'statusCode': 200,
        #     'browserHtml': '<html> ... </html>',
        # }