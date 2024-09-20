from django.urls import path
from .views import User_Survey, A_Survey

urlpatterns = [
    path("", User_Survey.as_view()),
    path("delete/<int:id>/", A_Survey.as_view()),
    path("view/", A_Survey.as_view()),
]
