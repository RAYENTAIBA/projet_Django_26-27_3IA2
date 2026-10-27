from django.shortcuts import render, get_object_or_404
from .models import Expedition
from django.views.generic import ListView

# Create your views here.

"""def liste_expeditions(request):
    expeditions = (
        Expedition.objects
        .filter(statut='publiee ')
        .select_related('entreprise')
        .order_by('-created_at')
    )
    print(expeditions)
    return render(request, 'expeditions/liste.html', {'expeditions': expeditions})
"""

class ListeViewExpedition(ListView):
    model = Expedition
    template_name = 'expeditions/liste.html'
    context_object_name = 'expeditions'
    def get_queryset(self):
        return (
        Expedition.objects
        .filter(statut='publiee ')
        .select_related('entreprise')
        .order_by('-created_at')
        )
    

def detail_expedition(request, reference):
    expedition = get_object_or_404(Expedition, reference=reference)
    offres = (expedition.offres.select_related('transporteur', 'vehicule').order_by('-date_proposition'))
    return render(request,'expeditions/detail.html',{'expedition': expedition, 'offres': offres},)  