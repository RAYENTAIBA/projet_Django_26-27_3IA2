from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView
from EntrepriseApp.mixins import TransporteurRequisMixin
from EntrepriseApp.models import Entreprise
from ExpeditionsApp.models import Expedition
from VehiculesApp.models import Vehicule
from .models import Offre


class OffreListView(ListView):
    model = Offre
    template_name = 'offres/liste.html'
    context_object_name = 'offres'

    def get_queryset(self):
        return Offre.objects.select_related('expedition', 'transporteur', 'vehicule').order_by('-date_proposition')


class OffreCreateView(TransporteurRequisMixin, CreateView):
    model = Offre
    fields = ['expedition', 'vehicule', 'prix', 'delai_jours']
    template_name = 'offres/form.html'

    def get_initial(self):
        initial = super().get_initial()
        expedition_id = self.request.GET.get('expedition')
        if expedition_id:
            initial['expedition'] = expedition_id
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Ne proposer que les expéditions réellement ouvertes aux offres
        form.fields['expedition'].queryset = Expedition.objects.filter(statut__startswith='publiee')
        # Ne proposer que les véhicules disponibles de l'entreprise courante
        form.fields['vehicule'].queryset = Vehicule.objects.filter(
            entreprise=self.get_entreprise_courante(), disponible=True
        )
        return form

    def form_valid(self, form):
        # transporteur : déterminé par l'utilisateur connecté, jamais fourni tel quel par le client
        form.instance.transporteur = self.get_entreprise_courante()
        try:
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e.messages)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('expeditions:detail', kwargs={'reference': self.object.expedition.reference})

    def get_entreprise_courante(self):
        return self.request.user.entreprise


class OffreDeleteView(LoginRequiredMixin, DeleteView):
    model = Offre
    template_name = 'offres/confirm_delete.html'
    context_object_name = 'offre'
    success_url = reverse_lazy('offres:liste')
