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

    #def __init__(self):
    # self.conn = pymongo.connector.connect(
    #     host = 'localhost',
    #     user = 'root',
    #     password = '',
    #     database = 'foodData'
    # )
    def __init__(self):
        # MongoDB connection parameters
        self.mongo_uri = 'mongodb://localhost:27017/'
        self.mongo_db = 'foodData'
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]



        #Create a text index on ingredients field - for full text search
       # self.db.foods.create.index("ingredients", pymongo.TEXT)
      #  self.db.foods.create_index("ingredients", pymongo.TEXT)

        self.db.foods.create_index("ingredients", unique=True)

    def process_item(self, item, spider):
        # Define MongoDB document
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

        # Insert document into MongoDB
        self.db.foods.insert_one(food_data)
        return item
    
    def close_spider(self, spider):
        self.client.close()