from django.urls import path
from .views import Register, Log_in, Log_out, Info

urlpatterns = [
    path('register/', Register.as_view()),
    path('logout/', Log_out.as_view()),
    path('login/', Log_in.as_view()),
    path('', Info.as_view())
]
