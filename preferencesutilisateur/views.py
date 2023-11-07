from django.shortcuts import render
import os 
import json
from django.conf import settings
from .models import PreferenceUtilisateur
from django.contrib import messages


def index(request):
    devise_data = []    
    file_path = os.path.join(settings.BASE_DIR, "currencies.json")

    with open(file_path, "r") as json_file:       
        data = json.load(json_file)       
        for k,v in data.items():
            devise_data.append({"name": k, "value": v})
            
    exists = PreferenceUtilisateur.objects.filter(user=request.user).exists()
    preferences_utilisateur = None
    
    if exists:
        preferences_utilisateur = PreferenceUtilisateur.objects.get(user=request.user)
        
    if request.method == "GET":        
        return render(request, "preferencesutilisateur/index.html", {"devises": devise_data, "preferences_utilisateur": preferences_utilisateur})
    else:
        devise = request.POST["devise"]
        
        if exists:
            preferences_utilisateur.devise=devise
            preferences_utilisateur.save()
        else:
            PreferenceUtilisateur.objects.create(user=request.user, devise=devise)
        messages.success(request, "Modification enregistrée.")
        return render(request, "preferencesutilisateur/index.html", {"devises": devise_data, "preferences_utilisateur": preferences_utilisateur})
        