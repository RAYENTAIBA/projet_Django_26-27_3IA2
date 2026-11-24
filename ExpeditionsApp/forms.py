from django import forms
from .models import Expedition

class ExpeditionForm(forms.ModelForm):
    class Meta:
        model = Expedition
        # entreprise, reference et statut : jamais fournis par le client
        fields = ['ville_depart', 'ville_arrivee', 'poids_kg', 'date_souhaite']
        widgets = {
            'date_souhaite': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
