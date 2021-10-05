from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Recipe, Category, Ingredient, SiteUser
from .forms import SiteUserRegisterForm, SiteUserLoginForm
from django.contrib.auth import login as auth_login
# Create your views here.


class RandomRecipeView(View):

    def get(self, request, *args, **kwargs):

        random_recipes = Recipe.objects.order_by('?')[:5]
        context = {
            'random_recipes' : random_recipes
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
        
        result_recipes = result_recipes.values()
        for recipe in result_recipes:
            recipe['favorite_flag'] = request.user.favorite_recipes.filter(pk=recipe['id']).exists()
           
        print(result_recipes)
        context = { 'result_recipes' : result_recipes }
        
        return render(request, 'recipe/search_result.html', context)

# レシピのお気に入り登録

class FavoriteRecipeRegisterView(View):

    def get(self, request, *args, **kwargs):

        favorite_recipe = Recipe.objects.get(id=self.request.GET['recipe_id'])
        request.user.favorite_recipes.add(favorite_recipe)

        return redirect("recipe:ingredient_result")


class MyRecipeIndexView(View):

    def get(self, request, *args, **kwargs):

        favorite_recipes = request.user.favorite_recipes.all().values()
        for recipe in favorite_recipes:
            recipe['favorite_flag'] = True
        context = { 'my_recipes': favorite_recipes }

        return render(request, 'recipe/my_recipe.html', context)



def MakeFavorite(request):

    import json
    from django.http import HttpResponse
    from .models import Recipe, SiteUser

    favorite_recipe = Recipe.objects.get(id=request.POST['recipe_id'])
    request.user.favorite_recipes.add(favorite_recipe)

    response_data = {}
    response_data["recipe_id"] = request.POST['recipe_id']
    
    json = json.dumps(response_data)
    print(json)
    return HttpResponse(json, content_type='application/json')


def DestroyFavorite(request):

    import json
    from django.http import HttpResponse
    from .models import Recipe, SiteUser

    favorite_recipe = Recipe.objects.get(id=request.POST['recipe_id'])
    request.user.favorite_recipes.remove(favorite_recipe)

    response_data = {}
    response_data["recipe_id"] = request.POST['recipe_id']
    
    json = json.dumps(response_data)
    print(json)
    return HttpResponse(json, content_type='application/json')


# 会員登録
class SiteUserRegisterView(View):
    def get(self, request, *args, **kwargs):
        context = {
            "form": SiteUserRegisterForm(),
        }
        return render(request, "recipe/siteUser/register.html", context)


    def post(self, request, *args, **kwargs):
        form = SiteUserRegisterForm(request.POST)
        if not form.is_valid():
            return render(request, "recipe/siteUser/register.html", {"form": form})

        new_site_user = form.save(commit=False)
        new_site_user.set_password(form.cleaned_data["password"])

        new_site_user.save()
        # messages.success(request, "会員登録が完了しました")
        # return redirect("app:site_user_login")
    

# ログイン
class SiteUserLoginView(View):
    def get(self, request, *args, **kwargs):
        context = {
            "form": SiteUserLoginForm(),
        }
        return render(request, "recipe/siteUser/login.html", context)

    def post(self, request, *args, **kwargs):

        form = SiteUserLoginForm(request.POST)
        if not form.is_valid():
            return render(request, "recipe/siteUser/login.html", {"form": form})

        login_site_user = form.get_site_user()

        auth_login(request, login_site_user)

        return redirect("recipe:ingredient_search")
