from django.core.management.base import BaseCommand
import requests
from recipe.models import Ingredient, Recipe, TodayIngredientOrder
from django.conf import settings
from django.db.models import Q, Value, F, CharField


class Command(BaseCommand):
    def handle(self, *args, **options):
        today_ingredient_order = TodayIngredientOrder.objects.all().first()
        today_order = today_ingredient_order.order
        all_ingredients = Ingredient.objects.all().order_by("pk")
        target_ingredient = all_ingredients[today_order]
        target_ingredient_api_id = target_ingredient.api_id

        rakuten_recipe_api_search_param = {
            "applicationId": [settings.RAKUTEN_RECIPE_API_ID],
            "categoryId": target_ingredient_api_id,
        }
        rakuten_recipe_api_responses = requests.get(
            settings.RAKUTEN_RECIPE_API_URL, rakuten_recipe_api_search_param
        ).json()
        # print(rakuten_recipe_api_responses)

        for recipe_result in rakuten_recipe_api_responses["result"]:

            img = recipe_result["foodImageUrl"]
            link = recipe_result["recipeUrl"]
            title = recipe_result["recipeTitle"]
            publish_day = recipe_result["recipePublishday"]
            cooking_time = recipe_result["recipeIndication"]
            description = recipe_result["recipeDescription"]
            recipe_api_id = recipe_result["recipeId"]

            if not Recipe.objects.filter(api_id=recipe_api_id).exists():

                recipe = Recipe.objects.create(
                    img=img,
                    link=link,
                    title=title,
                    publish_day=publish_day,
                    cooking_time=cooking_time,
                    description=description,
                    api_id=recipe_api_id,
                )
                recipe.ingredients.add(target_ingredient)

                hiragana_api_headers = {
                    "Content-Type": "application/json",
                }
                hiragana_api_search_params = (
                    '{"app_id":"' + settings.HIRAGANA_API_ID + '",'
                    '"sentence":"' + " ".join(recipe_result["recipeMaterial"]) + '",'
                    '"output_type":"hiragana"'
                    "}"
                )
                hiragana_api_response = requests.post(
                    settings.HIRAGANA_API_URL,
                    data=hiragana_api_search_params.encode("utf-8"),
                    headers=hiragana_api_headers,
                ).json()
                # print(hiragana_api_response)

                recipe_material_hiragana_list = hiragana_api_response[
                    "converted"
                ].split()
                for material_hiragana_name in recipe_material_hiragana_list:
                    ingredient = (
                        Ingredient.objects.annotate(
                            material_hiragana_name=Value(
                                material_hiragana_name, output_field=CharField()
                            )
                        )
                        .filter(
                            Q(material_hiragana_name__startswith=F("hiragana_name"))
                            | Q(material_hiragana_name__endswith=F("hiragana_name"))
                        )
                        .first()
                    )
                    if ingredient is not None:
                        recipe.ingredients.add(ingredient)

                recipe.save()
            else:
                print("既にそのレシピは登録されている")
                continue

        today_order += 1
        if all_ingredients.count() <= today_order:
            today_order = 0
        today_ingredient_order.order = today_order
        today_ingredient_order.save()
