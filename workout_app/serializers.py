from rest_framework.serializers import ModelSerializer
from .models import Workout, User_Workout
from exercise_app.serializers import ExerciseSerializer

class WorkoutSerializer(ModelSerializer):
    exercises = ExerciseSerializer(many=True)
    class Meta:
        model = Workout
        fields = ['id', 'workout_name', 'workout_details', 'exercises', 'created_by']

class UserWorkoutSerializer(ModelSerializer):
    workout_id = WorkoutSerializer()

    class Meta:
        model = User_Workout
        fields = ['user_id','workout_id',]