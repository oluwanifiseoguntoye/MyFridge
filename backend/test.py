import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myfridge.settings')
django.setup()

from recipesapi.models import Recipe, UserIngredient, RecipeIngredient

#create ingredients
flour = UserIngredient.objects.create(ingredient='flour')
sauce = UserIngredient.objects.create(ingredient='tomato sauce')
mozzarella = UserIngredient.objects.create(ingredient='mozzarella cheese')

pizza = Recipe.objects.create(
    recipe='Pizza', 
    description='A beautiful Italian Pizza',
    url = 'https://www.simplyrecipes.com/recipes/homemade_pizza/'
    )

RecipeIngredient.objects.create(recipe=pizza, ingredient=flour)
RecipeIngredient.objects.create(recipe=pizza, ingredient=sauce)
RecipeIngredient.objects.create(recipe=pizza, ingredient=mozzarella)