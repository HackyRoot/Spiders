import scrapy
import re, json

class ProductSpider(scrapy.Spider):
    name = 'product'
    allowed_domains = ['mediamarkt.de']
    start_urls = ['https://www.mediamarkt.de/de/category/qled-tvs-696.html']

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.mediamarkt.de/de/category/qled-tvs-696.html",
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

        with open("preloaded_state.json", "w") as outfile:
            json.dump(preloaded_state_json, outfile)

        category_id = re.findall(r'-(\d+)\.html', response.url)
        product_data = preloaded_state_json['apolloState']
        # total_products =

        category_query = 'categoryV4({' \
                            '"experiment":"mp",' \
                            '"page":1,' \
                            '"pimCode":"CAT_DE_MM_696\"})'
        cat_data_key = '$ROOT_QUERY.categoryV4({{"experiment":"mp","page":1,"wcsId":"{}"}})'.format(cat_id[0])


        # total_items =
