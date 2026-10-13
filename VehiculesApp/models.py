from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

# Create your models here.

class Vehicule(models.Model):
    immmatriculation=models.CharField(max_length=8, unique=True)  #"""validators=[MaxLengthValidator(10, "msg d'erreur")fct]"""
    type_vehicule=models.CharField(max_length=50,choices=[
        ('camion','camion'),
        ('camionette','camionette'),
        ('fourgon','fourgon'),
        ('remorque','remorque'),
        ('semi-remorque','semi-remorque'),
    ])
    capacite_kg=models.PositiveIntegerField(validators=[MinValueValidator(1,"Une capacité nulle ne peut pas être acceptée")])
    disponible=models.BooleanField(default=True)
    entreprise=models.ForeignKey('EntrepriseApp.Entreprise', on_delete=models.CASCADE, related_name='vehicules')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def clean(self):
        super().clean()
        if self.entreprise_id and self.entreprise.type_entreprise != "transporteur":
            raise ValidationError("Seuls les transporteurs peuvent avoir des vehicules")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    
