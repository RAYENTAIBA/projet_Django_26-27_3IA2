from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Entreprise, Utilisateur

class InscriptionForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Utilisateur
        fields = ('username', 'email', 'telephone')

class EntrepriseForm(forms.ModelForm):
    class Meta:
        model = Entreprise
        fields = ['raison_social', 'matricule_fiscal', 'type_entreprise', 'adresse', 'gerant']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # N'afficher que les utilisateurs qui n'ont pas encore d'entreprise (ou le gérant actuel en cas de modification)
        instance = kwargs.get('instance')
        gerants_occupes = Entreprise.objects.values_list('gerant_id', flat=True)
        if instance and instance.pk:
            gerants_occupes = gerants_occupes.exclude(pk=instance.pk)
        self.fields['gerant'].queryset = Utilisateur.objects.exclude(user_id__in=gerants_occupes)
