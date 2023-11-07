from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Achat, Categorie
from django.contrib import messages


@login_required(login_url="/authentication/connexion")
def index(request):
    categories = Categorie.objects.all()
    achats = Achat.objects.filter(proprietaire=request.user)
    context={
        "achats": achats,
    }
    return render(request, "achats/index.html", context)



def ajout_achat(request):
    categories = Categorie.objects.all()
    context = {
        "categories": categories,
        "values": request.POST,
    }
    if request.method == "GET":
        return render(request, "achats/ajoutachat.html", context)
    
    if request.method == "POST":
        montant = request.POST["montant"]
        
        if not montant:
            messages.error(request, "Le Montant est obligatoire")
            return render(request, "achats/ajoutachat.html", context)
        
        description = request.POST["description"]
        categorie = request.POST["categorie"]
        date = request.POST["date_achat"]
        
        if not description:
            messages.error(request, "La Description est obligatoire")
            return render(request, "achats/ajoutachat.html", context)
    Achat.objects.create(proprietaire=request.user, montant=montant, description=description, categorie=categorie, date=date)
    messages.success(request, "Achat enregistré avec succès!!!")
    
    return redirect("achats")
            


def editer_achat(request, id):
    achat = Achat.objects.get(pk=id)
    categories = Categorie.objects.all()
    context = {
        'achat': achat,
        'values': achat,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'achats/editerachat.html', context)
    if request.method == 'POST':
        montant = request.POST['montant']

        if not montant:
            messages.error(request, "Le Montant est obligatoire")
            return render(request, 'achats/editerachat.html', context)
        description = request.POST['description']
        categorie = request.POST['categorie']
        date = request.POST['date_achat']

        if not description:
            messages.error(request, "La Description est obligatoire")
            return render(request, 'achats/editerachat.html', context)

        achat.proprietaire = request.user
        achat.montant = montant
        achat.description = description
        achat.categorie = categorie
        achat. date = date

        achat.save()
        messages.success(request, "Edition effectuée avec succès!!!")

        return redirect('achats')



def supprimer_achat(request, id):
    achat = Achat.objects.get(pk=id)
    achat.delete()
    messages.success(request, "Achat Supprimé")
    return redirect("achats")
