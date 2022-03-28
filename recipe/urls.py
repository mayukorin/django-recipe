from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = "recipe"
urlpatterns = [
    path("recipes/random", views.RecipeRandomListView.as_view(), name="random_list"),
    path("categories", views.CategoryListView.as_view(), name="category_list"),
    path(
        "recipes/search_by_ingredient",
        views.RecipeSearchByIngredientListView.as_view(),
        name="search_by_ingredient_list",
    ),
    path("site_user/signup/", views.SignUpView.as_view(), name="site_user_signup"),
    path(
        "site_user/property_change/",
        views.UserPropertyChangeView.as_view(),
        name="site_user_property_change",
    ),
    path("site_user/signin/", views.SignInView.as_view(), name="site_user_signin"),
    path("site_user/signout/", views.SignOutView.as_view(), name="site_user_signout"),
    path("make_favorite/", views.FavoriteCreateView.as_view(), name="make_favorite"),
    path(
        "destroy_favorite/",
        views.FavoriteDestroyView.as_view(),
        name="destroy_favorite",
    ),
    path(
        "recipes/favorite", views.RecipeFavoriteListView.as_view(), name="favorite_list"
    ),
    path(
        "site_user/password_change/",
        views.PasswordEditView.as_view(),
        name="site_user_password_change",
    ),
    path(
        "ingredients/recognition",
        TemplateView.as_view(template_name="recipe/ingredient_recognition.html"),
        name="ingredient_recognition",
    ),
    path(
        "ingredients/search_by_english_name/",
        views.IngredientSearchByEnglishNameListView.as_view(),
        name="ingredient_search_by_english_name_list",
    ),
    path(
        "ingredients/vision_api_info/",
        views.IngredientVisionApiInfoView.as_view(),
        name="ingredient_vision_api_info",
    ),
]
