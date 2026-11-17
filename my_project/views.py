from django.shortcuts import render
from VehiculesApp.models import Vehicule
from ExpeditionsApp.models import Expedition
from EntrepriseApp.models import Entreprise
from OffresApp.models import Offre


def home(request):
    context = {
        'total_vehicules': Vehicule.objects.count(),
        'total_expeditions': Expedition.objects.count(),
        'expeditions_publiees': Expedition.objects.filter(statut__startswith='publiee').count(),
        'total_entreprises': Entreprise.objects.count(),
        'total_offres': Offre.objects.count(),
        'dernieres_expeditions': Expedition.objects.select_related('entreprise').order_by('-created_at')[:5],
        'derniers_vehicules': Vehicule.objects.select_related('entreprise').order_by('-created_at')[:5],
    }
    return render(request, 'home.html', context)


def homeWithName(request, nom):
    return home(request)
