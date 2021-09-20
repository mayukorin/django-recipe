from django.shortcuts import render
from django.views.generic import View
from .models import Recipe
# Create your views here.

class RandomRecipeView(View):

    def get(self, request, *args, **kwargs):

        random_recipe_list = Recipe.objects.all
        context = {
            'random_recipe_list' : random_recipe_list
        }
        
        return render(request, 'recipe/random.html', context)


class SearchRecipeForIngredientView(View):

    def get(self, request, *args, **kwargs):
        print("okkk")
        return render(request, 'recipe/search_for_ingredient.html')
