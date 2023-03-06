import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myfridge.settings')
django.setup()

from recipesapi.models import Recipe, UserIngredient, RecipeIngredient
import requests
from bs4 import BeautifulSoup

url = 'https://oluwanifiseoguntoye.github.io/Recipes/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

for recipe in soup.find_all('div', {'class': 'recipes'}):
    # Find recipe name
    recipe_name = recipe.find('h1', {'class': 'recipe_name'}).text.strip()

    # Check if recipe already exists in database
    existing_recipe = Recipe.objects.filter(recipe=recipe_name).first()
    if existing_recipe:
        continue

    # Create new recipe
    description = recipe.find('p', {'class': 'recipe-desc'}).text.strip()
    url = recipe.find('p', {'class': 'recipe-url'}).text.strip()
    new_recipe = Recipe.objects.create(recipe=recipe_name, description=description, url=url)

    # Find ingredients
    ingredients_list = [ingredient.text.strip() for ingredient in recipe.find('ul').find_all('li')]

    # Add ingredients to recipe
    for ingredient_name in ingredients_list:
        # Check if ingredient already exists in database
        existing_ingredient = UserIngredient.objects.filter(ingredient=ingredient_name).first()
        if not existing_ingredient:
            # Create new ingredient
            existing_ingredient = UserIngredient.objects.create(ingredient=ingredient_name)

        # Add ingredient to recipe
        RecipeIngredient.objects.create(recipe=new_recipe, ingredient=existing_ingredient)
