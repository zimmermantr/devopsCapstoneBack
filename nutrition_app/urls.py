from rest_framework.views import APIView
from django.urls import path
from .views import All_foods,A_food,An_ingredient
urlpatterns=[
    path('',All_foods.as_view(),name="all_foods"),
    path('<int:food_id>/',A_food.as_view(),name="a_food"),
    path('<int:food_id>/ingredient/<int:ingredient_id>/',An_ingredient.as_view(),name="an_ingredient"),
]