from django.contrib import admin
from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'recipe'
urlpatterns = [
    path('random', views.RecipeRandomListView.as_view(), name='random'),
    path('search_for_ingredient',
         views.CategoryListView.as_view(), name='ingredient_search'),
    path('result_for_ingredient',
         views.RecipeSearchByIngredientListView.as_view(), name='ingredient_result'),
    # path('siteUser/register', views.SiteUserRegisterView.as_view(), name='site_user_register'),
    path('siteUser/signup/', views.SignUpView.as_view(), name='site_user_signup'),
    path('siteUser/property-change/', views.UserPropertyChangeView.as_view(),
         name='site_user_property_change'),
    # path('siteUser/login', views.SiteUserLoginView.as_view(), name='site_user_login'),
    path('siteUser/signin/', views.SignInView.as_view(), name='site_user_signin'),
    # path('siteUser/logout', views.SiteUserLogoutView.as_view(), name='site_user_logout'),
    path('siteUser/signout/', views.SignOutView.as_view(),
         name='site_user_signout'),
    path('make_favorite/', views.FavoriteCreateView.as_view(), name='make_favorite'),
    path('destroy_favorite/', views.FavoriteDestroyView.as_view(),
         name='destroy_favorite'),
    path('favorite_recipe', views.RecipeFavoriteListView.as_view(),
         name='favorite_recipe'),
    path('siteUser/password-change/', views.PasswordEditView.as_view(),
         name='site_user_password_change'),
    path('ingredient_recognition', TemplateView.as_view(template_name='recipe/ingredient_recognition.html'),
         name='ingredient_recognition'),
    path('search_ingredient_by_english_name/', views.IngredientSearchByEnglishNameListView.as_view(
    ), name='ingredient_search_by_english_name'),
]
