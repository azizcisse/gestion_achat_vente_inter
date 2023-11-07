from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class Achat(models.Model):
    montant = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField() 
    proprietaire = models.ForeignKey(to=User, on_delete=models.CASCADE)
    categorie = models.CharField(max_length=266)
    
    def __str__(self):
        return self.category
    
    class Meta:
        ordering: ["-date"]
    
class Categorie(models.Model):
        nomCategorie = models.CharField(max_length=255) 
        
        class Meta:
            verbose_name_plural = "Categories"
        
        def __str__(self):
            return self.nomCategorie
