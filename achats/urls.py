from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="achats"),
    path("ajout-achat", views.ajout_achat, name="ajout-achat"),
    path("edit-achat/<int:id>", views.editer_achat, name="edit-achat"),
    path("supprimer-achat/<int:id>", views.supprimer_achat, name="supprimer-achat"),
]
