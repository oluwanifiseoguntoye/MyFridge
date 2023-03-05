from .models import Recipe, UserIngredient, RecipeIngredient
from rest_framework import serializers

class UserIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserIngredient
        fields = '__all__'

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = UserIngredientSerializer()

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient']

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ['recipe', 'ingredients', 'description', 'url']
