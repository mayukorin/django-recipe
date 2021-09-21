from django.shortcuts import render
from django.views.generic import View
from .models import Recipe, Category, Ingredient
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
        
        search_categories = Category.objects.all().prefetch_related('ingredients')
        context = { 'search_categories': search_categories }
        return render(request, 'recipe/search_for_ingredient.html', context)


class ResultRecipeForIngredientView(View):

    def get(self, request, *args, **kwargs):
        
        ingredient_id_list = self.request.GET.getlist('ingredients')
        result_recipes = Recipe.objects.filter()
        for ingredient_id in ingredient_id_list:
            result_recipes =result_recipes.filter(ingredients=ingredient_id)
        context = { 'result_recipes' : result_recipes }
        
        return render(request, 'recipe/search_result.html', context)
