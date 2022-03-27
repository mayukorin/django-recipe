from django.contrib.messages.api import success
from django.db.models.query_utils import FilteredRelation
from django.urls import reverse_lazy
from django.views.generic import View
from .models import Ingredient, Recipe, Category, SiteUser
from .forms import SignInForm, SignUpForm, UserPropertyChangeForm, PasswordEditForm
from django.contrib.auth import login as auth_login
import json
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView as AuthLoginView,
    PasswordChangeView as AuthPasswordChangeView,
)
from django.contrib.auth.views import LogoutView as AuthLogoutView
from django.views.generic import CreateView, ListView, UpdateView
from django.db.models import Q, FilteredRelation
from django.db.models import Count
from django.shortcuts import redirect, render


# Create your views here.


class RecipeRandomListView(ListView):

    model = Recipe
    context_object_name = "random_recipes"
    template_name = "recipe/random_recipe.html"
    paginate_by = 5

    def get_queryset(self, **kwargs):

        queryset = super().get_queryset(**kwargs)
        signin_user_pk = self.request.user.pk if self.request.user.is_authenticated else 0
        queryset = queryset.annotate(favorite_signin_user=FilteredRelation("favorite_users", condition=Q(favorite_users__pk=signin_user_pk)), 
            favorite_flag=Count("favorite_signin_user"),).order_by("?")
        return queryset
        


class CategoryListView(ListView):

    model = Category
    queryset = Category.objects.all().prefetch_related("ingredients")
    context_object_name = "search_categories"
    template_name = "recipe/search_for_ingredient.html"


class IngredientSearchByEnglishNameListView(View):

    def get(self, request, *args, **kwargs):

        ingredients_list = []
        print(self.request.GET.getlist("ingredient_english_names[]"))
        for ingredient_english_name in self.request.GET.getlist("ingredient_english_names[]"):
            ingredient = Ingredient.objects.filter(
                english_name=ingredient_english_name).first()
            print(ingredient)
            print(type(ingredient))
            if ingredient is not None:
                ingredient_id_and_name = {}
                ingredient_id_and_name['pk'] = ingredient.pk
                ingredient_id_and_name['name'] = ingredient.name
                ingredients_list.append(ingredient_id_and_name)
        print(ingredients_list)
        json_response = json.dumps(ingredients_list)
        return HttpResponse(json_response, content_type="application/json")


class RecipeSearchByIngredientListView(ListView):

    model = Recipe
    context_object_name = "result_recipes"
    template_name = "recipe/search_result_recipe.html"
    paginate_by = 5


    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        
        for ingredient_id in self.request.GET.getlist("ingredients"):
            queryset = queryset.filter(ingredients=ingredient_id)

        signin_user_pk = self.request.user.pk if self.request.user.is_authenticated else 0
        queryset = queryset.annotate(
            favorite_signin_user=FilteredRelation(
                "favorite_users", condition=Q(favorite_users__pk=signin_user_pk)
            ),
            favorite_flag=Count("favorite_signin_user"),
        )
        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        query_param = "&"
        for ingredient_id in self.request.GET.getlist("ingredients"):
            query_param += "ingredients=" + ingredient_id + "&"
        context.update({"query_param": query_param})
        return context


class RecipeFavoriteListView(LoginRequiredMixin, ListView):

    model = Recipe
    context_object_name = "favorite_recipes"
    template_name = "recipe/favorite_recipe.html"
    paginate_by = 5

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "ログインしてください", extra_tags="danger")
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        signin_user_pk = self.request.user.pk if self.request.user.is_authenticated else 0
        queryset = queryset.annotate(
            favorite_signin_user=FilteredRelation(
                "favorite_users", condition=Q(favorite_users__pk=signin_user_pk)
            ),
            favorite_flag=Count("favorite_signin_user"),
        ).filter(favorite_users__pk=signin_user_pk)
        return queryset


class FavoriteCreateView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "ログインしてください", extra_tags="danger")
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            favorite_recipe = Recipe.objects.get(id=request.POST["recipe_id"])
            request.user.favorite_recipes.add(favorite_recipe)

            response_data = {}
            response_data["recipe_id"] = request.POST["recipe_id"]

            json_response = json.dumps(response_data)
            return HttpResponse(json_response, content_type="application/json")


class FavoriteDestroyView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "ログインしてください", extra_tags="danger")
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            favorite_recipe = Recipe.objects.get(id=request.POST["recipe_id"])
            request.user.favorite_recipes.remove(favorite_recipe)

            response_data = {}
            response_data["recipe_id"] = request.POST["recipe_id"]

            json_response = json.dumps(response_data)
            return HttpResponse(json_response, content_type="application/json")


class SignInView(AuthLoginView):

    template_name = "recipe/siteUser/signin.html"
    authentication_form = SignInForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('recipe:random')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        response = super().post(request, *args, **kwargs)
        if self.get_form().is_valid():
            messages.success(request, "ログインしました")
        return response


class SignOutView(LoginRequiredMixin, AuthLogoutView):
    def dispatch(self, request, *args, **kwargs):

        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, "ログアウトしました")
        return response


class SignUpView(CreateView):

    model = SiteUser
    form_class = SignUpForm
    success_url = reverse_lazy("recipe:random")
    template_name = "recipe/siteUser/signup.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('recipe:random')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if self.object is not None:
            new_site_user = self.object
            new_site_user.set_password(new_site_user.password)
            new_site_user.save()
            auth_login(request, new_site_user)
            messages.success(self.request, "アカウント登録が完了しました")

        return response


'''
class UserPropertyChangeView(LoginRequiredMixin, UpdateView):

    model = SiteUser
    form_class = UserPropertyChangeForm
    success_url = reverse_lazy("recipe:random")
    template_name = "recipe/siteUser/property-change.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "ログインしてください", extra_tags="danger")
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if self.get_form().is_valid():
            messages.success(self.request, "アカウント情報を変更しました")

        return response

'''


class UserPropertyChangeView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "ログインしてください", extra_tags="danger")
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        form = UserPropertyChangeForm(instance=request.user)
        return render(request, 'recipe/siteUser/property-change.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserPropertyChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(self.request, "アカウント情報の変更が完了しました")
            return redirect('recipe:random')
        else:
            return render(request, 'recipe/siteUser/property-change.html', {'form': form})


class PasswordEditView(LoginRequiredMixin, AuthPasswordChangeView):

    form_class = PasswordEditForm
    template_name = "recipe/siteUser/password-change.html"
    success_url = reverse_lazy("recipe:random")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "ログインしてください", extra_tags="danger")
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.get_form().is_valid():
            # パスワードが変更される前に先に実行
            messages.success(self.request, "パスワードの変更が完了しました")
        response = super().post(request, *args, **kwargs)
        return response
