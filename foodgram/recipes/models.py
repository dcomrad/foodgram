from django.core.validators import MinValueValidator
from django.db import models

from ingredients.models import Ingredients
from tags.models import Tags
from users.models import User


class Recipes(models.Model):
    tags = models.ManyToManyField(
        to=Tags,
        through='TagsRecipes'
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    ingredients = models.ManyToManyField(
        to=Ingredients,
        related_name='recipes',
        through='IngredientsRecipes',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Изображение рецепта',
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
    )
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1, 'Значение не может быть меньше 1')],
        verbose_name='Время приготовления в минутах',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания рецепта'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class TagsRecipes(models.Model):
    tag = models.ForeignKey(
        to=Tags,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        to=Recipes,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.tag.name} - {self.recipe.name}'


class IngredientsRecipes(models.Model):
    ingredient = models.ForeignKey(
        to=Ingredients,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        to=Recipes,
        related_name='recipe_ingredients',
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField(
        verbose_name='Количество',
    )

    def __str__(self):
        return f'{self.ingredient.name}: {self.amount}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        to=User,
        related_name='cart',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        to=Recipes,
        related_name='cart',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.user.username}: {self.recipe.name}'

    class Meta:
        verbose_name = 'Корзина покупателя'


class Favorites(models.Model):
    user = models.ForeignKey(
        to=User,
        related_name='favorites',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        to=Recipes,
        related_name='favorites',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.user.username}: {self.recipe.name}'

    class Meta:
        verbose_name = 'Избранное покупателя'
