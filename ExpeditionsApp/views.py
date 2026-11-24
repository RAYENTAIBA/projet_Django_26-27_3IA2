from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from EntrepriseApp.mixins import ChargeurRequisMixin
from .models import Expedition
from .forms import ExpeditionForm


class ListeViewExpedition(ListView):
    model = Expedition
    template_name = 'expeditions/liste.html'
    context_object_name = 'expeditions'

    def get_queryset(self):
        return (
            Expedition.objects
            .filter(statut__startswith='publiee')
            .select_related('entreprise')
            .order_by('-created_at')
        )


class ExpeditionDetailView(DetailView):
    model = Expedition
    template_name = 'expeditions/detail.html'
    context_object_name = 'expedition'
    slug_field = 'reference'
    slug_url_kwarg = 'reference'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['offres'] = (
            self.object.offres
            .select_related('transporteur', 'vehicule')
        )
        return context


class ExpeditionsDeMonEntrepriseMixin:
    def get_queryset(self):
        return Expedition.objects.filter(entreprise=self.request.user.entreprise)


class ExpeditionCreateView(ChargeurRequisMixin, CreateView):
    model = Expedition
    form_class = ExpeditionForm
    template_name = 'expeditions/form.html'
    success_url = reverse_lazy('expeditions:liste')

    def form_valid(self, form):
        form.instance.entreprise = self.request.user.entreprise
        return super().form_valid(form)


class ExpeditionUpdateView(ChargeurRequisMixin, ExpeditionsDeMonEntrepriseMixin, UpdateView):
    model = Expedition
    form_class = ExpeditionForm
    template_name = 'expeditions/form.html'
    slug_field = 'reference'
    slug_url_kwarg = 'reference'
    success_url = reverse_lazy('expeditions:liste')


class ExpeditionDeleteView(ChargeurRequisMixin, ExpeditionsDeMonEntrepriseMixin, DeleteView):
    model = Expedition
    template_name = 'expeditions/confirm_delete.html'
    slug_field = 'reference'
    slug_url_kwarg = 'reference'
    context_object_name = 'expedition'
    success_url = reverse_lazy('expeditions:liste')
