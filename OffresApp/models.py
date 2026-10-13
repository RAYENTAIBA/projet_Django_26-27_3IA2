from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal

# Create your models here.

class Offre(models.Model):
    prix = models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(Decimal('0.001'), "Le prix doit être strictement supérieur à 0")])
    delai_jours = models.PositiveIntegerField(validators=[MinValueValidator(1, "Le délai doit être d'au moins 1 jour")])
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

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def clean(self):
        super().clean()

        # Règle 1 : L'entreprise doit être de type transporteur
        if self.transporteur_id and self.transporteur.type_entreprise != 'transporteur':
            raise ValidationError("Une offre ne peut être créée que par une entreprise dont le type est transporteur.")

        # Règle 2 : Le véhicule doit appartenir au transporteur de l'offre
        if self.vehicule_id and self.transporteur_id:
            if self.vehicule.entreprise_id != self.transporteur_id:
                raise ValidationError("Le véhicule associé doit appartenir au transporteur de l'offre.")

        # Règle 3 : Une expédition ne peut recevoir d'offres que si son statut est 'publiee'
        if not self.pk and self.expedition_id:
            if self.expedition.statut.strip() != 'publiee':
                raise ValidationError("Une expédition ne peut recevoir de nouvelles offres que si son statut est 'publiee'.")

        # Règle 4 : Pas deux offres 'proposee' de la même entreprise sur la même expédition
        if self.statut == 'proposee' and self.transporteur_id and self.expedition_id:
            doublon = Offre.objects.filter(
                expedition=self.expedition,
                transporteur=self.transporteur,
                statut='proposee'
            )
            if self.pk:
                doublon = doublon.exclude(pk=self.pk)
            if doublon.exists():
                raise ValidationError("Cette entreprise a déjà une offre au statut 'proposee' sur cette expédition.")

        # Règle 6 : Un véhicule non disponible ne peut pas être proposé sur une nouvelle offre
        if not self.pk and self.vehicule_id and not self.vehicule.disponible:
            raise ValidationError("Ce véhicule n'est pas disponible pour une nouvelle offre.")

        # Règle 7 : Compatibilité du type_vehicule avec le poids de l'expédition (en kg)
        if self.vehicule_id and self.expedition_id:
            # Table des correspondances (1 t = 1000 kg)
            limites_poids = {
                'camionnette': 1500,
                'camionette': 1500,
                'fourgon': 3500,
                'camion_porteur': 19000,
                'camion': 19000,
                'semi_remorque': 26000,
                'semi-remorque': 26000,
            }
            type_v = self.vehicule.type_vehicule
            poids = self.expedition.poids_kg
            limite_type = limites_poids.get(type_v)

            if limite_type and poids > limite_type:
                raise ValidationError(f"Le poids de l'expédition ({poids} kg) dépasse la capacité maximale pour un(e) {type_v} ({limite_type} kg).")
            
            if self.vehicule.capacite_kg and poids > self.vehicule.capacite_kg:
                raise ValidationError(f"Le poids de l'expédition ({poids} kg) dépasse la capacité du véhicule ({self.vehicule.capacite_kg} kg).")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

        # Règle 5 : Cascade à l'acceptation
        if self.statut == 'acceptee':
            # 1. L'expédition passe à 'attribuee'
            if self.expedition.statut != 'attribuee':
                self.expedition.statut = 'attribuee'
                self.expedition.save(update_fields=['statut'])

            # 2. Toutes les autres offres 'proposee' passent à 'refusee'
            Offre.objects.filter(
                expedition=self.expedition,
                statut='proposee'
            ).exclude(pk=self.pk).update(statut='refusee')


        
    


    def __str__(self):
        return f"Offre {self.id} {self.prix} {self.delai_jours} {self.statut} {self.date_proposition} {self.expedition.reference} {self.transporteur.raison_social} {self.vehicule.immmatriculation} {self.created_at} {self.updated_at}"
