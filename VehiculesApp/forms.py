from django import forms
from .models import Vehicule

class VehiculeForm(forms.ModelForm):
    class Meta:
        model = Vehicule
        fields = ['immmatriculation', 'type_vehicule', 'capacite_kg']
