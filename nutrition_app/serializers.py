from rest_framework import serializers
from .models import Food,Nutrient,Measurement,Ingredient

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['id','meal','user_id','created_at']

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id','name','measurement_id','amount_consumed','nutrients_id']

class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['amount','unit_name']

class NutrientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrient
        fields = ['name','measurement_id']
