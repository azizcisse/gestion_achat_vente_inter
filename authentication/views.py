from email.message import EmailMessage
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib import auth

from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import DefaultTokenGenerator, account_activation_token



class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data["email"]
        if not validate_email(email):
            return JsonResponse(
                {"email_error": "L'adresse email n'est pas valide."}, status=400
            )

        if User.objects.filter(email=email).exists():
            return JsonResponse(
                {
                    "email_error": "L'adresse email existe déjà, veuillez choisir un autre."
                },
                status=409,
            )

        return JsonResponse({"email_valid": True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data["username"]
        if not str(username).isalnum():
            return JsonResponse(
                {
                    "username_error": "Le nom d'utilisateur doit contenir que des caractères alphanumériques."
                },
                status=400,
            )

        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {
                    "username_error": "Le nom d'utilisateur existe déjà, veuillez choisir un autre."
                },
                status=409,
            )

        return JsonResponse({"username_valid": True})


class RegistrationView(View):
    def get(self, request):
        return render(request, "authentication/inscription.html")

    def post(self, request):
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        context = {"fieldValues": request.POST}

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(
                        request, "Le mot de passe doit avoir minimum 6 caractères."
                    )
                    return render(request, "authentication/inscription.html", context)
                user = User.objects.create_user(
                    username=username,
                    email=email,
                )
                user.set_password(password)
                user.is_active = False
                user.save()

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse(
                    "activercompte",
                    kwargs={
                        "uidb64": uidb64,
                        "token": account_activation_token.make_token(user),
                    },
                )

                activate_url = "http://" + domain + link

                email_body = (
                    "Salam "
                    + user.username
                    + " Veuillez utilisé ce lien pour vérifier votre compte\n"
                    + activate_url
                )

                email_subject = "Activer votre compte"
                email = EmailMessage(
                    email_subject,
                    email_body,
                    "nepasrepondre@africom.com",
                    [email],
                )
                email.send(fail_silently=False)

                messages.success(
                    request, "Félicitation, Le compte est créé avec succès!!!."
                )
                return render(request, "authentication/inscription.html")

        return render(request, "authentication/inscription.html")


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            
            if not account_activation_token.check_token(user, token):
                return redirect("connexion"+"?message="+"Le compte a déjà été activé.")
            
            if user.is_active:
                return redirect("connexion")
            user.is_active = True
            user.save()
            
            messages.success(request, "Votre a été activé avec succès.")
            return redirect("connexion")
            
        except Exception as e:
            raise e
        
        return redirect("conexion")


class LoginView(View):
    def get(self, request):
        return render(request, "authentication/connexion.html")
    
    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]  
            
        if username and password:           
            user = auth.authenticate(username=username, password=password)  
                    
            if user:
                
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, "Bienvenue, "+ user.username +" Vous etes actuellement connecté.")
                    return redirect("achats")
                    
                messages.error(request, "Vérifier votre adresse email, pour l'activation de votre compte.")
                return render(request, "authentication/connexion.html")
            
            messages.error(request, "Le Nom d'Utilisateur ou le Mot de Passe est inccorects, Reéssayer encore")
            return render(request, "authentication/connexion.html")
        
        messages.error(request, "S'il vous plait, veuillez remplir tous les champs.")
        return render(request, "authentication/connexion.html")
    
    
class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "Vous avez été déconnecté, Merci!")
        return redirect("connexion")
    