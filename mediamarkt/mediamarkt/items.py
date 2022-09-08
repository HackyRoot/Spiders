# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MediamarktItem(scrapy.Item):
    # define the fields for your item here like:
    product_name = scrapy.Field()
    product_id = scrapy.Field()
    product_price = scrapy.Field()
    product_url = scrapy.Field()
