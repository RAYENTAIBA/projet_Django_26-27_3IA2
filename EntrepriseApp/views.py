from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Entreprise
from .forms import EntrepriseForm


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


class EntrepriseCreateView(CreateView):
    model = Entreprise
    form_class = EntrepriseForm
    template_name = 'entreprises/form.html'
    success_url = reverse_lazy('entreprises:liste')


class EntrepriseUpdateView(UpdateView):
    model = Entreprise
    form_class = EntrepriseForm
    template_name = 'entreprises/form.html'
    success_url = reverse_lazy('entreprises:liste')


class EntrepriseDeleteView(DeleteView):
    model = Entreprise
    template_name = 'entreprises/confirm_delete.html'
    context_object_name = 'entreprise'
    success_url = reverse_lazy('entreprises:liste')
