# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter


class FoodscraperPipeline:
    def process_item(self, item, spider):
        return item


import pymongo

class SaveToMongoPipeline:
    def __init__(self):
        self.mongo_uri = 'mongodb+srv://root:root@fypcluster.zdqrt70.mongodb.net/?retryWrites=true&w=majority&appName=FYPCluster'
        self.mongo_db = 'ScrapedRecipes'
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]


    def process_item(self, item, spider):
        food_data = {
            "recipeId" : item["recipeId"],
            "url": item["url"],
            "title": item["title"],
            "description": item["description"],
            "image": item["image"],
            "prepTime": item["prepTime"],
            "cookTime": item["cookTime"],
            "ingredients": item["ingredients"],
            "steps": item["steps"],
        }

        self.db.foods.insert_one(food_data)
        return item
    
    def close_spider(self, spider):
        self.client.close()