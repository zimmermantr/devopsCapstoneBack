from django.db import models
from user_app.models import App_user
from workout_app.models import Workout

# from workout_app.models import Workout


class Workout_Program(models.Model):
    program_name = models.CharField(max_length=50)
    program_details = models.TextField()
    program_difficulty = models.CharField(max_length=20)
    program_duration = models.CharField(max_length=20)
    frequency_per_week = models.CharField(max_length=12)
    workouts = models.ManyToManyField(Workout, related_name="workout_programs", blank=True)
    created_by = models.ForeignKey(App_user, on_delete=models.CASCADE, blank=True, null=True)



class User_Workout_Program(models.Model):
    program_id = models.ForeignKey(Workout_Program, related_name="program_copy", on_delete=models.CASCADE)
    user_id = models.ForeignKey(App_user, related_name="userWorkoutPrograms", on_delete=models.CASCADE)
