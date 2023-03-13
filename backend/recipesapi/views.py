import ssl

ssl._create_default_https_context = ssl._create_unverified_context

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Recipe, UserIngredient, RecipeIngredient
from .serializers import RecipeSerializer
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import nltk 
import random
from nltk.tokenize import word_tokenize
from django.http import JsonResponse

class RecipeFilter(APIView):
    def post(self, request):
        ingredients = request.data.get('ingredients', [])
        if ingredients:
            recipes = Recipe.objects.all()
            for ingredient in ingredients:
                recipes = recipes.filter(ingredients__ingredient__ingredient__iexact=ingredient)
            serializer = RecipeSerializer(recipes, many=True)
            return Response(serializer.data)
        else:
            return Response({'message': 'Please provide a list of ingredients.'})


class RecipeList(APIView):
    def get(self, request):
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)
    

class RecipeBot(APIView):

    def post(self, request):
        message = request.data['message']
        
        # Initialize a chatbot instance
        bot = ChatBot('Bot')
        
        # Train the chatbot with recipes and their ingredients
        recipes = Recipe.objects.all()
        trainer = ListTrainer(bot)
        for recipe in recipes:
            trainer.train([recipe.recipe] + [ri.ingredient.ingredient for ri in recipe.ingredients.all()])
        
        # Extract the ingredients from the user message
        def extract_ingredients(message):
            ingredient_list = [ingredient.ingredient.lower() for ingredient in UserIngredient.objects.all()]
            words = nltk.word_tokenize(message.lower())
            ingredients = []
            for word in words:
                if word in ingredient_list:
                    ingredients.append(word)
            return ingredients
        
       # Filter recipes by ingredients
        def filter_recipes_by_ingredients(ingredients):
            recipes = Recipe.objects.all()
            filtered_recipes = []
            for recipe in recipes:
                recipe_ingredients = [ri.ingredient.ingredient.lower() for ri in recipe.ingredients.all()]
                if all(ingredient.lower() in recipe_ingredients for ingredient in ingredients):
                    filtered_recipes.append(recipe)
            return filtered_recipes      
        
        state = 'searching'
        current_recipe = None
        filtered_recipes = []

        # Return recipe description if recipe found
        def chatbot_response(state, message, current_recipe, filtered_recipes):


            if state == 'searching':
                ingredients = extract_ingredients(message)
                filtered_recipes = filter_recipes_by_ingredients(ingredients)

                if len(filtered_recipes) != 0:
                    print(filtered_recipes)
                    current_recipe = 0
                    random.shuffle(filtered_recipes)
                    current_recipe = filtered_recipes[0]
                    state = 'next_recipe'
                    print(state == 'next_recipe')
                    print('passed')
                    return state, current_recipe, filtered_recipes, JsonResponse({'message': current_recipe.description + " Here's the recipe's URL for preparation: " + current_recipe.url })
                
                # This line will only execute if filtered_recipes is empty
                print('passed')
                state = 'no_recipes'
                return state, current_recipe, filtered_recipes, JsonResponse({'message': "I'm sorry, there are currently no recipes available with those ingredients."})
            
            while state == 'next_recipe':
                    print('not passed')
                    affirmations = ['yes', 'sure', 'yeah']
                    negations = ['no', 'nope']
                    if any(word in message.lower() for word in affirmations):
                        current_recipe += 1
                        if current_recipe < len(filtered_recipes):
                            current_recipe = filtered_recipes[current_recipe]
                            return state, current_recipe, filtered_recipes, JsonResponse({'message': current_recipe.description + " Here's the recipe's URL for preparation: " + current_recipe.url + " Would you like another recipe instead?"})
                        else:
                            state = 'no_more_recipes'
                            return state, current_recipe, filtered_recipes, JsonResponse({'message': "I'm sorry, there are no more recipes with those ingredients. Enjoy cooking!"})
                        
                    elif any(word in message.lower() for word in negations):
                        state = 'end'
                        return state, current_recipe, filtered_recipes, JsonResponse({'message': "Okay, enjoy cooking!"})
                    
                    state = 'searching'
                    return state, current_recipe, filtered_recipes, JsonResponse({'message': "I'm sorry, I don't understand. Can you please rephrase your message?"})
            
        state, current_recipe, filtered_recipes, response = chatbot_response(state, message, current_recipe, filtered_recipes)
        return response

    