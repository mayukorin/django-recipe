from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class Category(models.Model):
    name = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100, default="")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, related_name="ingredients"
    )
    api_id = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=300, unique=True)
    img = models.CharField(max_length=300, unique=True)
    publish_day = models.CharField(max_length=100, default="")
    recipe_time = models.CharField(max_length=100, default="")
    description = models.CharField(max_length=100, default="")
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return self.title


class TodayIngredientOrder(models.Model):
    order = models.IntegerField(default=0)


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

    username = models.CharField(verbose_name="ユーザ名", max_length=150)

    email = models.EmailField(verbose_name="メールアドレス", unique=True)

    objects = SiteUserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [
        "username",
    ]

    favorite_recipes = models.ManyToManyField(Recipe, related_name="favorite_users")
