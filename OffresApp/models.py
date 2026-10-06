from django.db import models

# Create your models here.

class Offre(models.Model):
    prix=models.DecimalField(max_digits=10,decimal_places=3)
    delai_jours=models.PositiveIntegerField()
    statut=models.CharField(max_length=30,choices=[
        ('proposee','proposee'),
        ('acceptee','acceptee'),
        ('refusee','refusee'),
        ('retiree','retiree'),
    ], default='proposee')
    date_proposition=models.DateTimeField(auto_now_add=True)
    expedition=models.ForeignKey('ExpeditionsApp.Expedition', on_delete=models.CASCADE, related_name='offres')
    transporteur=models.ForeignKey('EntrepriseApp.Entreprise', on_delete=models.CASCADE, related_name='offres')
    vehicule=models.ForeignKey('VehiculesApp.Vehicule', on_delete=models.CASCADE, related_name='offres')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Offre {self.id} {self.prix} {self.delai_jours} {self.statut} {self.date_proposition} {self.expedition.reference} {self.transporteur.raison_social} {self.vehicule.reference} {self.created_at} {self.updated_at}"