# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FoodscraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field
   # pass


class FoodItem(scrapy.Item):
    recipeId = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    description =scrapy.Field()
    image = scrapy.Field()
    prepTime = scrapy.Field()
    cookTime = scrapy.Field()
    ingredients = scrapy.Field()
    steps = scrapy.Field()