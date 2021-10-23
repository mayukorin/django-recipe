from django.db.models.query_utils import FilteredRelation
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View
from .models import Ingredient, Recipe, Category, SiteUser
from .forms import SiteUserRegisterForm, SiteUserLoginForm, SignInForm, SignUpForm
from django.contrib.auth import login as auth_login, logout as auth_logout
import json
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.views import LogoutView as AuthLogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, ListView
from django.db.models import Q, FilteredRelation
from django.db.models import Count


# Create your views here.


class RandomRecipeView(ListView):

    model = Recipe
    context_object_name = 'random_recipes'
    template_name = 'recipe/random.html'

    def get(self, request, *args, **kwargs):
        self.user_pk = request.user.pk if request.user.is_authenticated else 0
        return super().get(request, *args, **kwargs)

    def get_queryset(self):

        queryset = Recipe.objects.annotate(favorite_login_user=FilteredRelation('favorite_users', condition=Q(favorite_users__pk=self.user_pk)), favorite_flag=Count('favorite_login_user')).order_by("?")[:5]
        return queryset
        


class SearchRecipeForIngredientView(ListView):
    
    model = Category
    queryset = Category.objects.all().prefetch_related("ingredients")
    context_object_name = 'search_categories'
    template_name = 'recipe/search_for_ingredient.html'


class ResultRecipeForIngredientView(ListView):

    model = Recipe
    context_object_name = 'result_recipes'
    template_name = 'recipe/search_result.html'

    def get(self, request, *args, **kwargs):
        self.user_pk = request.user.pk if request.user.is_authenticated else 0
        self.ingredient_id_list = self.request.GET.getlist("ingredients")
        print(self.ingredient_id_list)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Recipe.objects.filter()
        for ingredient_id in self.ingredient_id_list:
            queryset = queryset.filter(ingredients=ingredient_id)

        queryset = queryset.annotate(favorite_login_user=FilteredRelation('favorite_users', condition=Q(favorite_users__pk=self.user_pk)), favorite_flag=Count('favorite_login_user'))
        return queryset
    


class FavoriteRecipeIndexView(LoginRequiredMixin, ListView):

    permission_denied_message = "ログインしてください"
    model = Recipe
    context_object_name = 'favorite_recipes'
    template_name = 'recipe/favorite_recipe.html'


    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "ログインしてください", extra_tags='danger')
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        self.user_pk = request.user.pk if request.user.is_authenticated else 0
        return super().get(request, *args, **kwargs)

    def get_queryset(self):

        queryset = Recipe.objects.annotate(favorite_login_user=FilteredRelation('favorite_users', condition=Q(favorite_users__pk=self.user_pk)), favorite_flag=Count('favorite_login_user')).filter(favorite_users__pk=self.user_pk)
        return queryset


   


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


class SignInView(SuccessMessageMixin, AuthLoginView):

    template_name = 'recipe/siteUser/signin.html'
    authentication_form = SignInForm
    success_message = 'ログインしました'

class SignOutView(SuccessMessageMixin, AuthLogoutView):

    success_message = 'ログアウトしました'


class SignUpView(CreateView):

    model = SiteUser
    form_class = SignUpForm
    success_url = reverse_lazy('recipe:random')

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if self.object is not None:
            new_site_user = self.object
            new_site_user.set_password(new_site_user.password)
            new_site_user.save()
            auth_login(request, new_site_user)
            messages.success(self.request, 'アカウント登録が完了しました')
        
        return response

