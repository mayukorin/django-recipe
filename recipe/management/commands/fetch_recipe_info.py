from django.core.management.base import BaseCommand
import requests
from recipe.models import Ingredient, Recipe, TodayIngredientOrder


REQUEST_URL = "https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20170426"
APP_ID = "1054952264484319668"

class Command(BaseCommand):
    def handle(self, *args, **options):
        today_order_model = TodayIngredientOrder.objects.all()[0]
        today_order = today_order_model.order

        ingredients = Ingredient.objects.all().order_by('pk')
        target_ingredient = ingredients[today_order]
        target_api_id = target_ingredient.api_id

        search_param = {
            "applicationId":[APP_ID],
            #"formatVersion":2,
            "categoryId": target_api_id
        }
        responses = requests.get(REQUEST_URL, search_param).json()
        # print(responses["result"])

        for recipe_result in responses["result"]:
            img = recipe_result["foodImageUrl"]
            link = recipe_result["recipeUrl"]
            title = recipe_result["recipeTitle"]
            publish_day = recipe_result["recipePublishday"]
            recipe_time = recipe_result["recipeIndication"]
            description = recipe_result["recipeDescription"]

            try:
                recipe = Recipe.objects.create(img=img, link=link, title=title, publish_day=publish_day, recipe_time=recipe_time, description=description)
            except Exception as e:
                print("既にそのレシピは登録されている")
                continue
            # recipe.ingredients.add(target_ingredient)
            add_target_ingredient_flag = True
            for ingredient_name in recipe_result["recipeMaterial"]:
                if Ingredient.objects.filter(name=ingredient_name).exists():
                    ingredient = Ingredient.objects.get(name=ingredient_name)
                    if ingredient.id == target_ingredient.id:
                        add_target_ingredient_flag = False
                    recipe.ingredients.add(ingredient)

            if add_target_ingredient_flag:
                recipe.ingredients.add(target_ingredient)

                
            recipe.save()


        today_order += 1
        if ingredients.count() <= today_order:
            today_order = 0
        today_order_model.order = today_order
        today_order_model.save()
        