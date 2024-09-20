from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
from .serializers import WorkoutSerializer, Workout, User_Workout, UserWorkoutSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
# Create your views here.

class User_permissions(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class All_workouts(User_permissions):
    def get(self, request):
        workouts = Workout.objects.filter(created_by__in=[request.user.id]).order_by("pk")
        return Response(WorkoutSerializer(
                workouts, many=True,
            ).data)
    
    def post(self, request):
        new_workout = Workout(**request.data)
        new_workout.created_by = request.user
        new_workout.save()
        return Response(WorkoutSerializer(new_workout).data, status=HTTP_201_CREATED)
    
class A_workout(User_permissions):
    def get(self, request, workout_id):
        workout = get_object_or_404(Workout, id=workout_id)
        print(f'{request.user} is trying to access workouts')
        if workout.created_by.id not in [1,request.user.id]:
            return Response("not autorized", status=HTTP_400_BAD_REQUEST)
        return Response(WorkoutSerializer(workout).data)

    def put(self, request, workout_id):
        try:
            workout = Workout.objects.get(id=workout_id) #get_object_or_404(Exercise, id=exercise_id)
            if str(workout.created_by.id) != str(request.user.id):
                return Response("doesn't belong to user", status=HTTP_400_BAD_REQUEST)
            Workout.objects.filter(id=workout_id).update(**request.data)
            return Response(status=HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            return Response("something went wrong", status=HTTP_400_BAD_REQUEST)
        

    def delete(self, request,  workout_id):
        workout = Workout.objects.get(id=workout_id) #get_object_or_404(Exercise, id=exercise_id)
        if str(workout.created_by.id) != str(request.user.id):
            return Response("doesn't belong to user", status=HTTP_400_BAD_REQUEST)
        # Workout.objects.filter(id=workout_id).delete()
        workout.exercises.all().delete()
        workout.delete()
        return Response(status=HTTP_204_NO_CONTENT)