# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags
from itemloaders.processors import TakeFirst, MapCompose

def remove_text(value):
    return value.split('')[1]

class FragrancedirectItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    id = scrapy.Field()
    product_name = scrapy.Field()
    product_url = scrapy.Field()
    product_current_price = scrapy.Field()
    product_save = scrapy.Field()
