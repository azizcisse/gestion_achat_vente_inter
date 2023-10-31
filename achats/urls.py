from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="achats"),
    path("ajout-achat", views.ajout_achat, name="ajout-achat"),
]
