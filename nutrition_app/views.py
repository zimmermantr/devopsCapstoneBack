from django.shortcuts import render,get_object_or_404
from .models import Food, Ingredient, Measurement, Nutrient
from .serializers import FoodSerializer,IngredientSerializer,MeasurementSerializer,NutrientSerializer
from user_app.models import App_user
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK,HTTP_204_NO_CONTENT,HTTP_400_BAD_REQUEST,HTTP_404_NOT_FOUND,HTTP_201_CREATED
# Create your views here.
class All_foods(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # try:
            user = App_user.objects.get(username=self.request.user)
            all_foods = Food.objects.filter(user_id_id=user.id)
            serialized_food = FoodSerializer(all_foods, many=True)
            serialized_food_data = serialized_food.data
            for a_food in serialized_food_data:
                ingredients = Ingredient.objects.filter(food_id__id=a_food['id']) 
                serialized_ingredients = IngredientSerializer(ingredients, many=True)
                a_food['ingredients'] = serialized_ingredients.data
                
                for food_ingredient in a_food['ingredients']:
                    ingredient_measurement = Measurement.objects.get(id=food_ingredient['measurement_id'])
                    serialized_measurement = MeasurementSerializer(ingredient_measurement)
                    nutrients = Nutrient.objects.filter(id__in=food_ingredient['nutrients_id'])
                    serialized_nutrients = NutrientSerializer(nutrients, many=True)
                    
                    food_ingredient['measurement_id'] = serialized_measurement.data
                    food_ingredient['nutrients_id'] = serialized_nutrients.data
                    
                    for nutrient_item in food_ingredient['nutrients_id']:
                        nutrient_measurement = Measurement.objects.get(id=nutrient_item['measurement_id'])
                        serialized_measurement = MeasurementSerializer(nutrient_measurement)
                        nutrient_item['measurement_id'] = serialized_measurement.data 
                        
            return Response(serialized_food.data, status=HTTP_200_OK)
        # except:
        #     return Response(status=HTTP_404_NOT_FOUND)
        
class A_food(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,food_id):
            a_food = get_object_or_404(Food,id=food_id)
            serialized_food = FoodSerializer(a_food)
            serialized_food_data = serialized_food.data
            ingredient_list = Ingredient.objects.filter(food_id__id__contains = a_food.id)
            serialized_ingredients = IngredientSerializer(ingredient_list,many=True)
            serialized_food_data['ingredients'] = serialized_ingredients.data
            for ingredient in serialized_food_data['ingredients']:
                ingredient_measurement = Measurement.objects.get(id=ingredient['measurement_id'])
                serialized_measurement = MeasurementSerializer(ingredient_measurement)
                nutrients = Nutrient.objects.filter(id__in = ingredient['nutrients_id'])
                serialized_nutrients= NutrientSerializer(nutrients,many=True)
                ingredient['measurement_id'] = serialized_measurement.data
                ingredient['nutrients_id'] = serialized_nutrients.data
                for nutrient_item in ingredient['nutrients_id']:
                    nutrient_measurement = Measurement.objects.get(id=nutrient_item['measurement_id'])
                    serialized_measurement = MeasurementSerializer(nutrient_measurement)
                    nutrient_item['nutrients_id'] = serialized_measurement.data                    
            return Response(serialized_food_data,status=HTTP_200_OK)
    
    def post(self,request,food_id):
        try:
            user = App_user.objects.get(username=request.user)
            a_food = Food(user_id=user,meal=request.data['meal'])
            a_food.save()
            return Response(status=HTTP_201_CREATED)
        except:
            return Response(status=HTTP_400_BAD_REQUEST)
        
    def delete(self,request,food_id):
        try:
            user = App_user.objects.get(username=request.user)
            a_food = user.foods.get(id=food_id)
            a_food.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        except:
            return Response(status=HTTP_400_BAD_REQUEST)

class An_ingredient(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request,food_id,ingredient_id):
        # try:
            food = Food.objects.get(id=food_id)
            nutrient_list=request.data['ingredient']['foodNutrients']
            nutrients_to_add = []
            for nutrient in nutrient_list:
                nutrient_measurement = Measurement(amount=nutrient['value'],unit_name=nutrient['unitName'])
                nutrient_measurement.save()
                nutrient_description = Nutrient(name = nutrient['nutrientName'],measurement_id= nutrient_measurement)
                nutrient_description.save()
                nutrients_to_add.append(nutrient_description)
            ingredient_measurement = Measurement(amount=request.data['ingredient']['servingSize'],unit_name=request.data['ingredient']['servingSizeUnit'])
            ingredient_measurement.save()
            ingredient = Ingredient(name=request.data['ingredient']['description'],food_id=food,measurement_id=ingredient_measurement)
            ingredient.save()
            ingredient.nutrients_id.set(nutrients_to_add)
            serialized_ingredient = IngredientSerializer(ingredient)
            return Response(serialized_ingredient.data,status=HTTP_201_CREATED)
        # except:
        #     return Response(status=HTTP_400_BAD_REQUEST)
        
    def put(self,request,food_id,ingredient_id):
        try:
            a_food = Food.objects.get(id=food_id)
            ingredient = a_food.ingredients.get(id=ingredient_id)
            ingredient.amount_consumed = request.data['amount']
            ingredient.save()
            return Response(status=HTTP_204_NO_CONTENT)
        except:
            return Response(status=HTTP_400_BAD_REQUEST)

    def delete(self,request,food_id,ingredient_id):
        # try:
            a_food = Food.objects.get(id=food_id)
            ingredient = a_food.ingredients.get(id=ingredient_id)
            ingredient.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        # except:
        #     return Response(status=HTTP_404_NOT_FOUND)

