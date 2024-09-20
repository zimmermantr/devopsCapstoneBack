from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
from .serializers import WorkoutProgramSerializer, UserWorkoutProgramSerializer, User_Workout_Program, Workout_Program
from exercise_app.serializers import UserExerciseSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from workout_app.models import User_Workout
from exercise_app.models import User_Exercise
from user_app.models import App_user

# Create your views here.


class User_permissions(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class All_programs(User_permissions):
    def get(self, request):

        workout_programs = Workout_Program.objects.filter(created_by__in=[1,request.user.id]).order_by("pk")
        return Response(
            WorkoutProgramSerializer(
                workout_programs, many=True,
            ).data
        )

#       This allows the user to add a program from the db and make a copy of it for their account without changin the db
    def post(self, request):
        user = request.user
        if request.data.get("program_id"):
            program_id = request.data.get("program_id")
            existing_program = user.userWorkoutPrograms.filter(program_id=program_id).first()
            if not existing_program:
                program = get_object_or_404(Workout_Program, pk=program_id)
                new_user_program = User_Workout_Program(program_id=program, user_id=user)
                new_user_program.save()
                serializer = UserWorkoutProgramSerializer(new_user_program)
                return Response(serializer.data, status=HTTP_201_CREATED)
            else:
                return Response("You already have this program added.", status=HTTP_204_NO_CONTENT)
            #Allows user to create custom programs, could be used later
        # else:
        #     new_workout_program = Workout_Program(**request.data)
        #     new_workout_program.created_by = request.user
        #     new_workout_program.save()
        #     return Response(WorkoutProgramSerializer(new_workout_program).data, status=HTTP_201_CREATED)

# class A_program(User_permissions):
#     def get(self, request, id):
#         workout_program = get_object_or_404(User_Workout_Program, program_id=id)
#         serializer = UserWorkoutProgramSerializer(workout_program)
#         print(serializer.created_by)
#         if workout_program.created_by not in [1,request.user.id]:
#             return Response("not autorized", status=HTTP_400_BAD_REQUEST)
#         return Response(serializer.data)
class A_program(User_permissions):
    def get(self, request, id):
        workout_program = get_object_or_404(Workout_Program, id=id)
        program_created_by = workout_program.created_by  # Access the creator from the related program
        
        if program_created_by != request.user and program_created_by.id != 1:
            return Response("not authorized", status=HTTP_400_BAD_REQUEST)
        serializer = WorkoutProgramSerializer(workout_program)
        return Response(serializer.data)

    def put(self, request, id):
        try:
            workout_program = Workout_Program.objects.get(id=id)
            # print(workout_program)
            if str(workout_program.created_by.id) != str(request.user.id):
                return Response("doesn't belong to user", status=HTTP_400_BAD_REQUEST)
            Workout_Program.objects.filter(id=id).update(**request.data)
            return Response(status=HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            return Response("something went wrong", status=HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        a_user_program = get_object_or_404(request.user.userWorkoutPrograms, program_id=id)
        a_user_program.delete()
        # workout_program = get_object_or_404(Workout_Program, id=id)
        return Response(status=HTTP_204_NO_CONTENT)
        