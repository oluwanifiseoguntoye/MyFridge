from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Recipe, UserIngredient
from .serializers import UserIngredientSerializer, RecipeSerializer
from rest_framework import status

@api_view(['POST'])
def ingredient_create(request):
    ingredients_str = request.data.get('ingredients')
    ingredients_list = ingredients_str.split(',')
    ingredient_data = []
    for ingredient in ingredients_list:
        serializer = UserIngredientSerializer(data={'name': ingredient.strip()})
        if serializer.is_valid():
            serializer.save()
            ingredient_data.append(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': f"{len(ingredients_list)} ingredients created successfully", 'ingredients': ingredient_data}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def recipe_list(request):
    user_ingredients = request.GET.getlist('ingredients')
    recipes = Recipe.objects.filter(ingredients__ingredient__name__in=user_ingredients)

    serializer = RecipeSerializer(recipes, many=True)
    return Response(serializer.data)

