from rest_framework.serializers import ModelSerializer
from .models import Exercise, User_Exercise

class ExerciseSerializer(ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'exercise_name', 'force', 'sets', 'reps', 'difficulty', 'equipment', 'instructions', 'primary_muscle', 'secondary_muscle', 'start_img', 'end_img', 'gif_img', 'created_by']

class UserExerciseSerializer(ModelSerializer):
    exercise_id = ExerciseSerializer()

    class Meta:
        model = User_Exercise
        fields = ['exercise_id',]