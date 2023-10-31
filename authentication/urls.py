from .views import RegistrationView 
from django.urls import path 


urlpatterns = [
    path("inscription", RegistrationView.as_view(), name="inscription"),
]
