from django.core.management.base import BaseCommand
import requests
from recipe.models import Ingredient, Recipe, TodayIngredientOrder
from django.conf import settings
from django.db.models import Q, Value, F, CharField
import time

class Command(BaseCommand):
    def handle(self, *args, **options):
        today_order_model = TodayIngredientOrder.objects.all()[0]
        today_order = today_order_model.order

        ingredients = Ingredient.objects.all().order_by('pk')
        target_ingredient = ingredients[today_order]
        # target_api_id = target_ingredient.api_id
        for target_ingredient in ingredients:
            target_api_id = target_ingredient.api_id
            print(target_api_id)
            if target_api_id == '0':
                break
            time.sleep(1)

            search_param = {
                "applicationId":[settings.RAKUTEN_RECIPE_API_ID],
                #"formatVersion":2,
                "categoryId": target_api_id
            }
            responses = requests.get(settings.RAKUTEN_RECIPE_API_URL, search_param).json()
            print(responses)
            for i, recipe_result in enumerate(responses["result"]):
                if i >= 1:
                    continue
                img = recipe_result["foodImageUrl"]
                link = recipe_result["recipeUrl"]
                title = recipe_result["recipeTitle"]
                publish_day = recipe_result["recipePublishday"]
                cooking_time = recipe_result["recipeIndication"]
                description = recipe_result["recipeDescription"]
                api_recipe_id = recipe_result["recipeId"]
                
                if Recipe.objects.filter(api_id=api_recipe_id).count() == 0:
                    recipe = Recipe.objects.create(img=img, link=link, title=title, publish_day=publish_day, cooking_time=cooking_time, description=description, api_id=api_id)
                    add_target_ingredient_flag = True
                    recipe_material_sentence = " ".join(recipe_result["recipeMaterial"])
                    print(recipe_material_sentence)
                    headers = {
                        'Content-Type': 'application/json',
                    }
                    data = '{"app_id":"' + settings.HIRAGANA_API_ID + '",' \
                    '"sentence":"' + recipe_material_sentence + '",' \
                        '"output_type":"hiragana"' \
                        '}'
                    response = requests.post(
                        settings.HIRAGANA_API_URL, 
                        data=data.encode("utf-8"), 
                        headers=headers,
                    ).json()
                    # print(response)
                    recipe_material_hiragana_list = response["converted"].split()
                    for material_hiragana_name in recipe_material_hiragana_list:
                        ingredient = Ingredient.objects.annotate(
                            japa=Value(material_hiragana_name, output_field=CharField())
                        ).filter(Q(japa__startswith=F('hiragana_name')) | Q(japa__endswith=F('hiragana_name'))).first()
                        if ingredient is not None:
                            recipe.ingredients.add(ingredient)

                    if add_target_ingredient_flag:
                        recipe.ingredients.add(target_ingredient)
                    recipe.save()
                else:
                    print("既にそのレシピは登録されている")
                    continue
                # recipe.ingredients.add(target_ingredient)


        today_order += 1
        if ingredients.count() <= today_order:
            today_order = 0
        today_order_model.order = today_order
        today_order_model.save()
        