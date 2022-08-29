# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from w3lib.html import remove_tags
from itemloaders.processors import TakeFirst, MapCompose


def remove_special_char(value):
    return value.replace('#', '').strip()


class AmazonukItem(scrapy.Item):
    # define the fields for your item here like:
    rank = scrapy.Field(input_processor=MapCompose(remove_tags, remove_special_char), output_processor=TakeFirst())
    book_title = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    author = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
