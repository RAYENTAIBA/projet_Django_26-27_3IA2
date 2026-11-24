from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from EntrepriseApp.mixins import TransporteurRequisMixin
from .models import Vehicule
from .forms import VehiculeForm


class VehiculesDeMonEntrepriseMixin:
    def get_queryset(self):
        return Vehicule.objects.filter(entreprise=self.request.user.entreprise)


class VehiculeListView(ListView):
    model = Vehicule
    template_name = 'vehicules/list.html'
    context_object_name = 'vehicules'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'entreprise') and user.entreprise and user.entreprise.type_entreprise == 'transporteur':
            return Vehicule.objects.filter(entreprise=user.entreprise).order_by('-created_at')
        return Vehicule.objects.select_related('entreprise').order_by('-created_at')


class VehiculeCreateView(TransporteurRequisMixin, CreateView):
    model = Vehicule
    template_name = 'vehicules/form.html'
    form_class = VehiculeForm
    success_url = reverse_lazy('vehicules:liste')

    def form_valid(self, form):
        form.instance.entreprise = self.request.user.entreprise
        return super().form_valid(form)


class VehiculeUpdateView(TransporteurRequisMixin, VehiculesDeMonEntrepriseMixin, UpdateView):
    model = Vehicule
    template_name = 'vehicules/form.html'
    form_class = VehiculeForm
    success_url = reverse_lazy('vehicules:liste')


class VehiculeDeleteView(TransporteurRequisMixin, VehiculesDeMonEntrepriseMixin, DeleteView):
    model = Vehicule
    template_name = 'vehicules/confirm_delete.html'
    context_object_name = 'vehicule'
    success_url = reverse_lazy('vehicules:liste')


# Alias pour rétro-compatibilité
DeleteViewVehicule = VehiculeDeleteView
