from django.contrib import admin
from .models import Category, Ingredient, SiteUser, Recipe, TodayIngredientOrder

# Register your models here.

admin.site.register(SiteUser)
admin.site.register(Recipe)
admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(TodayIngredientOrder)