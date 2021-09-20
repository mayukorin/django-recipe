from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=100, default="category")

class Ingredient(models.Model):
    name = models.CharField(max_length=100, default="inredient")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=300)
    img = models.CharField(max_length=300)
    ingredients = models.ManyToManyField(Ingredient)
   
    # クラスオブジェクトを文字列で返すメソッド
    def __str__(self):
        return self.title


class SiteUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class SiteUser(AbstractUser):


    username = models.CharField(_("username"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), unique=True)

    objects = SiteUserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    favorite_recipes = models.ManyToManyField(Recipe, blank=True)
