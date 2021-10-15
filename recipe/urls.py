from django.contrib import admin
from django.urls import path
from . import views
app_name = 'recipe'
urlpatterns = [
    path('random', views.RandomRecipeView.as_view(), name='random'), 
    path('search_for_ingredient', views.SearchRecipeForIngredientView.as_view(), name='ingredient_search'),
    path('result_for_ingredient', views.ResultRecipeForIngredientView.as_view(), name='ingredient_result'),
    # path('siteUser/register', views.SiteUserRegisterView.as_view(), name='site_user_register'),
    path('siteUser/signup', views.SignUpView.as_view(), name='site_user_signup'),
    # path('siteUser/login', views.SiteUserLoginView.as_view(), name='site_user_login'),
    path('siteUser/signin', views.SignInView.as_view(), name='site_user_signin'),
    # path('siteUser/logout', views.SiteUserLogoutView.as_view(), name='site_user_logout'),
    path('siteUser/signout', views.SignOutView.as_view(), name='site_user_signout'),
    path('make_favorite/', views.MakeFavoriteView.as_view(), name='make_favorite'),
    path('destroy_favorite/', views.DestroyFavoriteView.as_view(), name='destroy_favorite'),
    path('favorite_recipe', views.FavoriteRecipeIndexView.as_view(), name='favorite_recipe'),
]
