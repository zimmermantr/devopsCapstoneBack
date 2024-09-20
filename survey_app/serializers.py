from rest_framework import serializers
from .models import Survey_response


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey_response
        fields = [
            "id",
            "user_id",
            "height",
            "weight",
            "age",
            "gender",
            "activity_level",
            "dietary_restrictions",
            "equipment",
            "created",
        ]
