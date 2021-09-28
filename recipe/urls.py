from django.contrib import admin
from django.urls import path, include
from . import views
app_name = 'recipe'
urlpatterns = [
    path('random', views.RandomRecipeView.as_view(), name='random'), 
    path('search_for_ingredient', views.SearchRecipeForIngredientView.as_view()),
    path('result_for_ingredient', views.ResultRecipeForIngredientView.as_view(), name='ingredient_result'),
    path('siteUser/register', views.SiteUserRegisterView.as_view(), name='site_user_register')
]
