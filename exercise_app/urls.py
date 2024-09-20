from django.urls import path
from .views import All_exercises, An_exercise

urlpatterns = [
    path('', All_exercises.as_view()),
    path("<int:exercise_id>/", An_exercise.as_view()),
]