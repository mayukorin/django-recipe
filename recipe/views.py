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
        print("okkk")
        search_categories = Category.objects.all().prefetch_related('ingredients')
        context = { 'search_categories': search_categories }
        return render(request, 'recipe/search_for_ingredient.html', context)


class ResultRecipeForIngredientView(View):

    def get(self, request, *args, **kwargs):
        ingredients = self.request.GET.getlist('ingredients')
        print(ingredients)
        search_categories = Category.objects.all().prefetch_related('ingredients')
        context = { 'search_categories': search_categories }
        return render(request, 'recipe/search_for_ingredient.html', context)
