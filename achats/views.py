from django.shortcuts import render



def index(request):
    return render(request, "achats/index.html")

def ajout_achat(request):
    return render(request, "achats/ajoutachat.html")