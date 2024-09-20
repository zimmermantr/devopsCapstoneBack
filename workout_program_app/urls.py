from django.urls import path, include
from .views import All_programs, A_program

urlpatterns = [
    path('', All_programs.as_view()),
    path('<int:id>/', A_program.as_view()),
    path('<int:id>/workouts/', include('workout_app.urls')),
]