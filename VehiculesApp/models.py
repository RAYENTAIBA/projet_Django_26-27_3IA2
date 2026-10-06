from django.db import models

# Create your models here.

class Vehicule(models.Model):
    immmatriculation=models.CharField(max_length=8, unique=True)
    type_vehicule=models.CharField(max_length=50,choices=[
        ('camion','camion'),
        ('camionette','camionette'),
        ('fourgon','fourgon'),
        ('remorque','remorque'),
        ('semi-remorque','semi-remorque'),
    ])
    capacite_kg=models.PositiveIntegerField()
    disponible=models.BooleanField(default=True)
    entreprise=models.ForeignKey('EntrepriseApp.Entreprise', on_delete=models.CASCADE, related_name='vehicules')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    
