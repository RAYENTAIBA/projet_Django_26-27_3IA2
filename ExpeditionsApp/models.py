from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


# Create your models here.

class Expedition(models.Model):
    reference=models.CharField(max_length=12, unique=True ,editable=False)
    ville_depart=models.CharField(max_length=50)
    ville_arrivee=models.CharField(max_length=50)
    date_proposition=models.DateTimeField(auto_now_add=True)
    date_souhaite=models.DateTimeField()
    poids_kg = models.PositiveIntegerField(validators=[MinValueValidator(1, "Le poids ne peut pas être nul")])
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

    def clean(self):
        super().clean()
        if self.entreprise_id and self.entreprise.type_entreprise != "chargeur":
            raise ValidationError("L'entreprise doit être de type chargeur")


    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference=self._generate_ref()
        self.full_clean()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_ref(cls): #methode interne convention "_" bech tnajem testa3malha fi west l class mouch lbara
        annee=timezone.now().strftime('%y')
        prefixe=f'EXP{annee}'
        last_value=(
            cls.objects
            .filter(reference__startswith=prefixe)
            .order_by('-reference')
            .first()
        )
        c=int(last_value.reference[-5:])+1 if last_value else 1
        if c > 99999:
            raise ValidationError(f'Limite de 99999 expedition atteinte pour l\'annne {annee}')
        
        


    """"def __str__(self):
        return f"Expedition {self.id} {self.reference} {self.ville_depart} 
        {self.ville_arrivee} {self.date_proposition} {self.date_souhaite} {self.poids_kg} 
        {self.statut} {self.entreprise.raison_social} {self.entreprise.matricule_fiscal} 
        {self.entreprise.type_entreprise} {self.entreprise.gerant.user_id} {self.entreprise.gerant.email} 
        {self.entreprise.gerant.telephone} {self.entreprise.gerant.created_at} {self.entreprise.gerant.updated_at} 
        {self.entreprise.adresse} {self.entreprise.created_at} {self.entreprise.updated_at}" """
    
    
    
    
    