from django.urls import path, include
from .views import All_workouts, A_workout

urlpatterns = [
    path('', All_workouts.as_view()),
    path('<int:workout_id>/', A_workout.as_view()),
    path('<int:workout_id>/exercises/', include('exercise_app.urls'))
]