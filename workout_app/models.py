from django.db import models
from user_app.models import App_user
from exercise_app.models import Exercise


# Create your models here.


class Workout(models.Model):
    workout_name = models.CharField()
    workout_details = models.TextField()
    # exercises, linked to Exercise
    # parent_program = models.ManyToManyField(
    #     Workout_Program, related_name="workouts", blank=True
    # )
    exercises = models.ManyToManyField(Exercise, related_name="workouts", blank=True)

    created_by = models.ForeignKey(App_user, on_delete=models.CASCADE, blank=True, null=True, related_name="custom_workouts")


class User_Workout(models.Model):
    workout_id = models.ForeignKey(
        Workout, related_name="workout_copy", on_delete=models.CASCADE
    )
    user_id = models.ForeignKey(
        App_user, related_name="userWorkouts", on_delete=models.CASCADE
    )
