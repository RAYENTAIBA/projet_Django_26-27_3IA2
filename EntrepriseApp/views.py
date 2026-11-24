from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Entreprise
from .forms import EntrepriseForm, InscriptionForm


class InscriptionView(CreateView):
    form_class = InscriptionForm
    template_name = 'registration/inscription.html'
    success_url = reverse_lazy('entreprises:ajouter')

    def form_valid(self, form):
        response = super().form_valid(form)  # crée l'utilisateur (self.object)
        login(self.request, self.object)     # ouvre directement sa session
        return response


class EntrepriseListView(ListView):
    model = Entreprise
    template_name = 'entreprises/liste.html'
    context_object_name = 'entreprises'

    def get_queryset(self):
        return Entreprise.objects.select_related('gerant').order_by('-created_at')


class EntrepriseDetailView(DetailView):
    model = Entreprise
    template_name = 'entreprises/detail.html'
    context_object_name = 'entreprise'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.type_entreprise == 'transporteur':
            context['vehicules'] = self.object.vehicules.all()
            context['offres'] = self.object.offres.select_related('expedition', 'vehicule')
        elif self.object.type_entreprise == 'chargeur':
            context['expeditions'] = self.object.expeditions.all()
        return context


class EntrepriseCreateView(LoginRequiredMixin, CreateView):
    model = Entreprise
    fields = ['raison_social', 'matricule_fiscal', 'type_entreprise', 'adresse']
    template_name = 'entreprises/form.html'
    success_url = reverse_lazy('expeditions:liste')

    def form_valid(self, form):
        form.instance.gerant = self.request.user
        return super().form_valid(form)


class EntrepriseUpdateView(LoginRequiredMixin, UpdateView):
    model = Entreprise
    form_class = EntrepriseForm
    template_name = 'entreprises/form.html'
    success_url = reverse_lazy('entreprises:liste')


class EntrepriseDeleteView(LoginRequiredMixin, DeleteView):
    model = Entreprise
    template_name = 'entreprises/confirm_delete.html'
    context_object_name = 'entreprise'
    success_url = reverse_lazy('entreprises:liste')
