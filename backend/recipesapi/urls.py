from django.urls import path
from .views import RecipeFilter, RecipeList, RecipeBot

urlpatterns = [
    path('recipes/', RecipeList.as_view(), name='recipe-list'),
    path('recipes/filter/', RecipeFilter.as_view(), name='recipe-filter'),
    path('recipebot/', RecipeBot.as_view(), name='chatbot'),
]