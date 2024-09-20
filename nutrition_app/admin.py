from django.contrib import admin
from .models import Measurement, Nutrient, Food, Ingredient

admin.site.register(Measurement)
admin.site.register(Nutrient)
admin.site.register(Food)
admin.site.register(Ingredient)

# Register your models here.
