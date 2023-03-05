from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Recipe, UserIngredient, RecipeIngredient
from .serializers import RecipeSerializer

class RecipeFilter(APIView):
    def post(self, request):
        ingredient_name = request.data.get('ingredient_name', None)
        if ingredient_name:
            recipes = Recipe.objects.filter(ingredients__ingredient__ingredient=ingredient_name)
            serializer = RecipeSerializer(recipes, many=True)
            return Response(serializer.data)
        else:
            return Response({'message': 'Please provide an ingredient name.'})

class RecipeList(APIView):
    def get(self, request):
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)


