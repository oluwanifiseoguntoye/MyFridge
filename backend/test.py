import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myfridge.settings')
django.setup()


from recipesapi.models import Recipe, UserIngredient, RecipeIngredient

# create ingredients
egg = UserIngredient.objects.create(name='egg')
bacon = UserIngredient.objects.create(name='bacon')
bread = UserIngredient.objects.create(name='bread')
cheese = UserIngredient.objects.create(name='cheese')
lettuce = UserIngredient.objects.create(name='lettuce')

# create recipes
omelette = Recipe.objects.create(name='Omelette')
club_sandwich = Recipe.objects.create(name='Club Sandwich')
cheeseburger = Recipe.objects.create(name='Cheeseburger')

# add recipe ingredients
RecipeIngredient.objects.create(recipe=omelette, ingredient=egg)
RecipeIngredient.objects.create(recipe=omelette, ingredient=cheese)

RecipeIngredient.objects.create(recipe=club_sandwich, ingredient=bread)
RecipeIngredient.objects.create(recipe=club_sandwich, ingredient=lettuce)
RecipeIngredient.objects.create(recipe=club_sandwich, ingredient=bacon)

RecipeIngredient.objects.create(recipe=cheeseburger, ingredient=bread)
RecipeIngredient.objects.create(recipe=cheeseburger, ingredient=lettuce)
RecipeIngredient.objects.create(recipe=cheeseburger, ingredient=cheese)
