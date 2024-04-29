import scrapy
from foodscraper.items import FoodItem

#
#The following code is based on a Scrapy tutorial
# the tutorial scraped books from https://books.toscrape.com/, a website to practice web scraping.
# I used to knowledge gained from this tutorial to create a Scrapy spider and use it on the 
#BBC Good Food website https://www.bbcgoodfood.com/. to scrape recipes. 
#with additional features incorporated and modifications made for my project demands
#

class FoodspiderSpider(scrapy.Spider):
    name = "foodspider"
    allowed_domains = ["www.bbcgoodfood.com"]
    start_urls = ["https://www.bbcgoodfood.com/search?q=dinner"]

    # set the initial page count to 1
    page_count = 1
    id = 1
    

    def parse(self, response):
        food_collection = response.css('article.card')
        for food in food_collection:
            relative_url = food.css('div a').attrib['href']

            food_url = 'https://www.bbcgoodfood.com' + relative_url
            yield response.follow(food_url, callback=self.parse_food_page)

    def parse_food_page(self, response):
        prep_list = response.css('.recipe__cook-and-prep .list .body-copy-small time')
        ingredients_list = response.css('.recipe__ingredients .list .pb-xxs')
        method_list = response.css('.recipe__method-steps .grouped-list .grouped-list__list .pb-xs')
        all_ingredients = []
        food_item = FoodItem()
        for ingredient in ingredients_list:
            ingredient = ingredient.css('::text').getall()
            ingredient_string = ' '.join(ingredient)
            all_ingredients.append(ingredient_string)


        food_item['recipeId'] = FoodspiderSpider.id
        FoodspiderSpider.id +=1

        food_item['url'] = response.url
        food_item['title'] = response.css('.headline h1 ::text').get()
        food_item['description'] = response.css('.post-header__body .editor-content ::text').get()
        food_item['image'] = response.css('div .post-header__image-container  picture img').attrib['src']
        food_item['prepTime'] = prep_list[0].css('::text').get()
        food_item['cookTime'] =  prep_list[1].css('::text').get()
        food_item['ingredients'] = all_ingredients
        food_item['steps'] =  response.css('.recipe__method-steps .grouped-list .grouped-list__list .pb-xs ::text').getall()

        yield food_item

        
        ## Limit to 2 pages
        FoodspiderSpider.page_count +=1
        next_page = FoodspiderSpider.page_count
        if next_page < 50:
            next_page_url = 'https://www.bbcgoodfood.com/search?q=dinner&page=' + str(next_page)
            print("Next page URL: ") 
            print(next_page_url) 
            yield response.follow(next_page_url, callback = self.parse)




        #             yield {
        #     'url' : response.url,
        #     'title' : response.css('.headline h1 ::text').get(),
        #     'description' : response.css('.post-header__body .editor-content ::text').get(),
        #     'prep_time' : prep_list[0].css('::text').get(),
        #     'cook_time' : prep_list[1].css('::text').get(),
        #     'ingredients' : all_ingredients,
        #     'steps' : response.css('.recipe__method-steps .grouped-list .grouped-list__list .pb-xs ::text').getall(),
        # }
        # yield FoodItem