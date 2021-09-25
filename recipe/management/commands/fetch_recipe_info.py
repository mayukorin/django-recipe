from django.core.management.base import BaseCommand
import requests
from recipe.models import Ingredient, Recipe


REQUEST_URL = "https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20170426"
APP_ID = "1054952264484319668"

class Command(BaseCommand):
    def handle(self, *args, **options):
        print("ok")
        search_param = {
            "applicationId":[APP_ID],
            #"formatVersion":2,
            "categoryId": "10-276"
        }
        responses = requests.get(REQUEST_URL, search_param).json()
        print(responses["result"])

        for recipe_result in responses["result"]:
            img = recipe_result["foodImageUrl"]
            link = recipe_result["recipeUrl"]
            title = recipe_result["recipeTitle"]
            recipe = Recipe.objects.create(img=img, link=link, title=title)
            
            for ingredient_name in recipe_result["recipeMaterial"]:
                if Ingredient.objects.filter(name=ingredient_name).exists():
                    ingredient = Ingredient.objects.get(name=ingredient_name)
                    recipe.ingredients.add(ingredient)

                
            recipe.save()