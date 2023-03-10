import ssl

ssl._create_default_https_context = ssl._create_unverified_context

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Recipe, UserIngredient, RecipeIngredient
from .serializers import RecipeSerializer
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import nltk 
import string
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


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
            print("Input message:", message)
            print("Tokenized words:", words)
            print("Ingredients found:", ingredients)
            return ingredients


        
        ingredients = extract_ingredients(message)
        
       # Filter recipes by ingredients
        def filter_recipes_by_ingredients(ingredients):
            recipes = Recipe.objects.all()
            filtered_recipes = []
            for recipe in recipes:
                recipe_ingredients = [ri.ingredient.ingredient.lower() for ri in recipe.ingredients.all()]
                if any(ingredient.lower() in recipe_ingredients for ingredient in ingredients):
                    filtered_recipes.append(recipe)
            print(filtered_recipes)
            return filtered_recipes

        filtered_recipes = filter_recipes_by_ingredients(ingredients)

        # Return recipe description if recipe found
        if filtered_recipes:
            recipe = filtered_recipes[0]
            serializer = RecipeSerializer(recipe)
            return Response({'message': serializer.data['description']})
        else:
            return Response({'message': "I'm sorry, there are currently no recipes available with those ingredients."})
