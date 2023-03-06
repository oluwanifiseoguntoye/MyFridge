from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Recipe, UserIngredient, RecipeIngredient
from .serializers import RecipeSerializer

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


