from rest_framework.serializers import ModelSerializer
from .models import App_user
from exercise_app.serializers import UserExerciseSerializer
from workout_app.serializers import UserWorkoutSerializer
from workout_program_app.serializers import UserWorkoutProgramSerializer
from survey_app.serializers import SurveySerializer


class UserSerializer(ModelSerializer):
    userWorkoutPrograms = UserWorkoutProgramSerializer(many = True)
    userWorkouts = UserWorkoutSerializer(many=True) 
    userExercises = UserExerciseSerializer(many=True)
    survey_responses = SurveySerializer(many=True)

    class Meta:
        model = App_user
        fields = ['id', 'email', 'userWorkoutPrograms', 'userWorkouts', 'userExercises','survey_responses']


class UserOnlySerializer(ModelSerializer):
    class Meta:
        model = App_user
        fields = ['id', 'email']
