from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST
)
from .serializers import Exercise, User_Exercise ,ExerciseSerializer, UserExerciseSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from workout_app.models import Workout

# Create your views here.

class User_permissions(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class All_exercises(User_permissions):

    # def get(self, request, workout_id):
    #     return Response(
    #         UserExerciseSerializer(
    #             get_object_or_404(request.user.user_workouts, id=workout_id).exercises.order_by("id"), many=True,
    #         ).data
    #     )
    
    def get(self, request):
        exercises = Exercise.objects.filter(created_by__in=[request.user.id]).order_by("pk")
        return Response(
            ExerciseSerializer(
                exercises, many=True,
            ).data
        )

    def post(self, request, workout_id):
        workout = get_object_or_404(request.user.custom_workouts, id=workout_id)
        new_exercise = Exercise(**request.data)
        new_exercise.created_by = request.user
        new_exercise.save()
        new_exercise.workouts.add(workout)
        return Response(ExerciseSerializer(new_exercise).data, status=HTTP_201_CREATED)


class An_exercise(User_permissions):
    
    def get(self, request, exercise_id):
        exercise = get_object_or_404(Exercise, id=exercise_id)
        if exercise.created_by.id not in [1,request.user.id]:
            return Response("not autorized", status=HTTP_400_BAD_REQUEST)
        return Response(ExerciseSerializer(exercise).data)

    def put(self, request, exercise_id):
        try:
            exercise = Exercise.objects.get(id=exercise_id) #get_object_or_404(Exercise, id=exercise_id)
            if str(exercise.created_by.id) != str(request.user.id):
                return Response("doesn't belong to user", status=HTTP_400_BAD_REQUEST)
            Exercise.objects.filter(id=exercise_id).update(**request.data)
            return Response(status=HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            return Response("something went wrong", status=HTTP_400_BAD_REQUEST)

    def delete(self, request, exercise_id):
        exercise = Exercise.objects.get(id=exercise_id) #get_object_or_404(Exercise, id=exercise_id)
        if str(exercise.created_by.id) != str(request.user.id):
            return Response("doesn't belong to user", status=HTTP_400_BAD_REQUEST)
        exercise.delete()
        return Response(status=HTTP_204_NO_CONTENT)