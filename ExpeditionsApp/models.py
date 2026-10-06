from django.db import models

# Create your models here.

class Expedition(models.Model):
    reference=models.CharField(max_length=8, unique=True ,editable=False)
    ville_depart=models.CharField(max_length=50)
    ville_arrivee=models.CharField(max_length=50)
    date_proposition=models.DateTimeField(auto_now_add=True)
    date_souhaite=models.DateTimeField()
    poids_kg=models.PositiveIntegerField()
    statut=models.CharField(max_length=50,choices=[
        ('publiee ','publiee'),
        ('attribuee','attribuee'),
        ('en cours','en cours'),
        ('livree','livree'),
        ('annulee','annulee')],
        default='publiee')
    entreprise=models.ForeignKey('EntrepriseApp.Entreprise',on_delete=models.CASCADE, related_name='expeditions')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Expedition {self.id} {self.reference} {self.ville_depart} {self.ville_arrivee} {self.date_proposition} {self.date_souhaite} {self.poids_kg} {self.statut} {self.entreprise.raison_social} {self.entreprise.matricule_fiscal} {self.entreprise.type_entreprise} {self.entreprise.gerant.user_id} {self.entreprise.gerant.email} {self.entreprise.gerant.telephone} {self.entreprise.gerant.created_at} {self.entreprise.gerant.updated_at} {self.entreprise.adresse} {self.entreprise.created_at} {self.entreprise.updated_at}"
    
    
    
    
    