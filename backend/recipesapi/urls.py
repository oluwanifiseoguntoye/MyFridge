from django.urls import path
from .views import RecipeFilter, RecipeList

urlpatterns = [
    path('recipes/', RecipeList.as_view(), name='recipe-list'),
    path('recipes/filter/', RecipeFilter.as_view(), name='recipe-filter'),
]