from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Recipe, Category
from .forms import SiteUserRegisterForm, SiteUserLoginForm, LoginForm
from django.contrib.auth import login as auth_login, logout as auth_logout
import json
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.


class RandomRecipeView(View):
    def get(self, request, *args, **kwargs):

        random_recipes = Recipe.objects.order_by("?")[:5]
        context = {"random_recipes": random_recipes}

        return render(request, "recipe/random.html", context)


class SearchRecipeForIngredientView(View):
    def get(self, request, *args, **kwargs):

        search_categories = Category.objects.all().prefetch_related("ingredients")
        context = {"search_categories": search_categories}
        return render(request, "recipe/search_for_ingredient.html", context)


class ResultRecipeForIngredientView(View):
    def get(self, request, *args, **kwargs):

        ingredient_id_list = self.request.GET.getlist("ingredients")
        result_recipes = Recipe.objects.filter()
        for ingredient_id in ingredient_id_list:
            result_recipes = result_recipes.filter(ingredients=ingredient_id)

        result_recipes = result_recipes.values()
        for recipe in result_recipes:
            recipe["favorite_flag"] = request.user.is_favorite_recipe(recipe["id"])

        context = {"result_recipes": result_recipes}

        return render(request, "recipe/search_result.html", context)


class FavoriteRecipeIndexView(LoginRequiredMixin, View):

    permission_denied_message = "ログインしてください"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "ログインしてください", extra_tags='danger')
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):

        favorite_recipes = request.user.favorite_recipes.all().values()
        for recipe in favorite_recipes:
            recipe["favorite_flag"] = True
        context = {"favorite_recipes": favorite_recipes}

        return render(request, "recipe/favorite_recipe.html", context)


class MakeFavoriteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            favorite_recipe = Recipe.objects.get(id=request.POST["recipe_id"])
            request.user.favorite_recipes.add(favorite_recipe)

            response_data = {}
            response_data["recipe_id"] = request.POST["recipe_id"]

            json_response = json.dumps(response_data)
            return HttpResponse(json_response, content_type="application/json")


class DestroyFavoriteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            favorite_recipe = Recipe.objects.get(id=request.POST["recipe_id"])
            request.user.favorite_recipes.remove(favorite_recipe)

            response_data = {}
            response_data["recipe_id"] = request.POST["recipe_id"]

            json_response = json.dumps(response_data)
            return HttpResponse(json_response, content_type="application/json")


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
        messages.success(request, "会員登録が完了しました")
        return redirect("recipe:site_user_login")


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
        messages.success(request, "ログインしました")
        print(request.POST.get('next'))
        return redirect("recipe:ingredient_search")

class LoginView(SuccessMessageMixin, AuthLoginView):

    template_name = 'recipe/siteUser/login.html'
    authentication_form = LoginForm
    success_message = 'ログインしました'


# ログアウト
class SiteUserLogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            auth_logout(request)

        messages.success(request, "ログアウトしました")

        return redirect("recipe:site_user_login")
