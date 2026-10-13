from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils import timezone


# Create your models here.

def validate_email(email):
    if not email:
        raise ValidationError("email est obligatoire")
    if not email.endswith('@gmail.com'):
        raise ValidationError("Seuls les emails appartenant au domaine gmail.com sont acceptés")

class Utilisateur(AbstractUser):
    user_id=models.CharField(max_length=8, editable=False, primary_key=True)
    email=models.EmailField(unique=True, validators=[validate_email])
    role=models.CharField(max_length=20, choices=[
        ('chargeur','chargeur'),
        ('transporteur','transporteur'),
        ('administrateur','administrateur')], default='chargeur')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    telephone=models.CharField(max_length=8)
    REQUIRED_FIELDS = ['email', 'telephone']

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = self.generate_id()
        self.full_clean()
        super().save(*args, **kwargs)

    @classmethod
    def generate_id(cls):
        # AA : 2 derniers chiffres de l'année (ex: 26 pour 2026) -> %y
        annee = timezone.now().strftime("%y")
        prefixe = f"{annee}user"
        
        last_value = (
            cls.objects.filter(user_id__startswith=prefixe)
            .order_by('user_id')
            .last()
        )
        
        # Compteur séquentiel 00-99 remis à zéro chaque année
        c = int(last_value.user_id[-2:]) + 1 if last_value else 0
        if c > 99:
            raise ValidationError(f"Le compteur d'utilisateurs a dépassé la limite maximale pour l'année 20{annee}.")
        
        return f"{prefixe}{c:02d}"

    def __str__(self):
        return f"{self.user_id} {self.email} {self.telephone} {self.role} {self.created_at} {self.updated_at}"
    



matricule_fiscal_validator=RegexValidator(regex=r'^\d{7}[/ -]?[A-Za-z][/ -]?[ABDNPEabdnpe][/ -]?[MPCNEmpcne][/ -]?\d{3}$', 
                                          message="Format du matricule fiscal invalide")
class Entreprise(models.Model):
    raison_social=models.CharField(max_length=100)
    matricule_fiscal = models.CharField(max_length=100, unique=True, validators=[matricule_fiscal_validator])
    type_entreprise=models.CharField(max_length=15,choices=[
        ('chargeur','chargeur'),
        ('transporteur','transporteur'),
    ])
    adresse=models.TextField(validators=[MinLengthValidator(20,"L'adresse doit contenir au moins 20 caracteres")])
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    gerant=models.OneToOneField(Utilisateur,on_delete=models.CASCADE,related_name='entreprise')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    
    def __str__(self):
        return f"Entreprise {self.id} {self.raison_social} {self.matricule_fiscal} {self.type_entreprise} {self.gerant.user_id} {self.gerant.email} {self.gerant.telephone} {self.gerant.created_at} {self.gerant.updated_at} {self.adresse} {self.created_at} {self.updated_at}"
    
    
    
    