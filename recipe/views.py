from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Recipe, Category, Ingredient
from .forms import SiteUserRegisterForm, SiteUserLoginForm
from django.contrib.auth import login as auth_login
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
