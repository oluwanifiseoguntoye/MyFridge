from django.urls import path
from . import views

urlpatterns = [
    path('ingredients/', views.ingredient_create),
    path('recipes/', views.recipe_list),
]