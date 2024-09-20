from django.db import models
from user_app.models import App_user

class Measurement(models.Model):
    amount = models.PositiveBigIntegerField(null=False,default=0)
    unit_name = models.CharField(null=False,blank=False)

class Nutrient(models.Model):
    name = models.CharField(null=False,blank=False,max_length=255)
    measurement_id = models.ForeignKey(Measurement, on_delete=models.CASCADE, related_name='nutrient_measurements')

class Food(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    meal = models.CharField(null=False,max_length=255)
    user_id = models.ForeignKey(App_user,related_name='foods', on_delete=models.CASCADE)

class Ingredient(models.Model):
    name = models.CharField(null=False,blank=False, max_length=255)
    amount_consumed = models.PositiveBigIntegerField(default=0)
    food_id = models.ForeignKey(Food,on_delete=models.CASCADE, related_name='ingredients',default=1 )
    measurement_id = models.ForeignKey(Measurement, on_delete=models.CASCADE, related_name='ingredient_measurements')
    nutrients_id = models.ManyToManyField(Nutrient, related_name='nutrients')