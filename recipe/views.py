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
from django.views.generic import CreateView, ListView
from django.db.models import Q, FilteredRelation, Value, F, CharField
from django.db.models import Count
from django.shortcuts import redirect, render
import requests
from django.conf import settings
from django.db.models.functions import Concat
import time


# Create your views here.


class RecipeRandomListView(ListView):

    model = Recipe
    context_object_name = "random_recipes"
    template_name = "recipe/random_recipe_list.html"
    paginate_by = 5

    def get_queryset(self, **kwargs):

        queryset = super().get_queryset(**kwargs)
        print(queryset)
        signin_user_pk = (
            self.request.user.pk if self.request.user.is_authenticated else 0
        )
        queryset = queryset.annotate(
            favorite_signin_user=FilteredRelation(
                "favorite_users", condition=Q(favorite_users__pk=signin_user_pk)
            ),
            favorite_flag=Count("favorite_signin_user"),
        )
        print(queryset)
        return queryset


class CategoryListView(ListView):

    model = Category
    queryset = Category.objects.all().prefetch_related("ingredients")
    context_object_name = "search_categories"
    template_name = "recipe/category_list.html"


class IngredientVisionApiInfoView(View):
    def post(self, request, *args, **kwargs):
        # start_time = time.perf_counter()
        responses = requests.post(
            settings.VISION_API_URL, request.POST["search_param"]
        ).json()

        '''
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(elapsed_time)
        print("Labelサーチ")
        '''
        return HttpResponse(json.dumps(responses), content_type="application/json")


class IngredientSearchByEnglishNameListView(View):
    def get(self, request, *args, **kwargs):
        # start_time = time.perf_counter()
        ingredient_pk_and_name_list = []

        for object_english_name_detected in self.request.GET.getlist(
            "object_english_name_list_detected[]"
        ):
            ingredient_pk_and_name = Ingredient.objects.filter(
                english_name=object_english_name_detected
            ).values("pk", "name")
            if len(ingredient_pk_and_name) == 1:
                ingredient_pk_and_name_list.append(ingredient_pk_and_name[0])

        json_response = json.dumps(ingredient_pk_and_name_list)
        '''
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(elapsed_time)
        print("英語サーチ")
        '''
        return HttpResponse(json_response, content_type="application/json")


class HiraganaConversionView(View):
    def get(self, request, *args, **kwargs):
        
        # start_time = time.perf_counter()
        
        texts_detected_string = ' '.join(self.request.GET.getlist("text_list_detected[]")).replace('"', '')

        headers = {
            'Content-Type': 'application/json',
        }
        data = '{"app_id":"' + settings.HIRAGANA_API_ID + '",' \
        '"sentence":"' + texts_detected_string + '",' \
            '"output_type":"hiragana"' \
            '}'
        response = requests.post(
            settings.HIRAGANA_API_URL, 
            data=data.encode("utf-8"), 
            headers=headers,
        ).json()

        hiragana_texts_detected_list = response["converted"].split()
        
        '''
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(elapsed_time)
        print("変換サーチ")
        '''
        return HttpResponse(json.dumps(hiragana_texts_detected_list), content_type="application/json")

class IngredientSearchByHiraganaNameListView(View):
    def post(self, request, *args, **kwargs):
        
        # start_time = time.perf_counter()
        ingredient_pk_and_name_list = []
        
        for hiragana_text_detected in self.request.POST.getlist(
            "hiragana_text_detected_list[]"
        ):

            ingredient_pk_and_name = Ingredient.objects.annotate(
                hiragana_text_detected=Value(hiragana_text_detected, output_field=CharField())
            ).filter(Q(hiragana_text_detected__startswith=F('hiragana_name')) | Q(hiragana_text_detected__endswith=F('hiragana_name'))).distinct().values("pk", "name")
            if len(ingredient_pk_and_name) == 1:
                ingredient_pk_and_name_list.append(ingredient_pk_and_name[0])
        
        json_response = json.dumps(ingredient_pk_and_name_list)
        '''
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(elapsed_time)
        print("ひらがなサーチ")
        '''
        return HttpResponse(json_response, content_type="application/json")





class RecipeSearchByIngredientListView(ListView):

    model = Recipe
    context_object_name = "result_recipes"
    template_name = "recipe/recipe_search_by_ingredient_list.html"
    paginate_by = 5

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)

        for ingredient_id in self.request.GET.getlist("ingredients"):
            queryset = queryset.filter(ingredients=ingredient_id)

        signin_user_pk = (
            self.request.user.pk if self.request.user.is_authenticated else 0
        )
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
    template_name = "recipe/recipe_favorite_list.html"
    paginate_by = 5

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "ログインしてください", extra_tags="danger")
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        signin_user_pk = (
            self.request.user.pk if self.request.user.is_authenticated else 0
        )
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
            return HttpResponse(json.dumps({}), content_type="application/json")


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
            favorite_recipe_cnt = request.user.favorite_recipes.count()
            return HttpResponse(json.dumps({"favorite_recipe_cnt": favorite_recipe_cnt}), content_type="application/json")


class SignInView(AuthLoginView):

    template_name = "recipe/site_user/signin.html"
    authentication_form = SignInForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("recipe:random_list")
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
    success_url = reverse_lazy("recipe:random_list")
    template_name = "recipe/site_user/signup.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("recipe:random_list")
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


class UserPropertyChangeView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "ログインしてください", extra_tags="danger")
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        form = UserPropertyChangeForm(instance=request.user)
        return render(request, "recipe/site_user/property_change.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = UserPropertyChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(self.request, "アカウント情報の変更が完了しました")
            return redirect("recipe:random_list")
        else:
            return render(
                request, "recipe/site_user/property_change.html", {"form": form}
            )


class PasswordEditView(LoginRequiredMixin, AuthPasswordChangeView):

    form_class = PasswordEditForm
    template_name = "recipe/site_user/password_change.html"
    success_url = reverse_lazy("recipe:random_list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "ログインしてください", extra_tags="danger")
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.get_form().is_valid():

            messages.success(self.request, "パスワードの変更が完了しました")
        response = super().post(request, *args, **kwargs)
        return response
