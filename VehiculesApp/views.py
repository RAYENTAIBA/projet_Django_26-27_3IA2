from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Vehicule
from .forms import VehiculeForm


class VehiculeListView(ListView):
    model = Vehicule
    template_name = 'vehicules/list.html'
    context_object_name = 'vehicules'

    def get_queryset(self):
        return Vehicule.objects.select_related('entreprise').order_by('-created_at')


class VehiculeCreateView(CreateView):
    model = Vehicule
    template_name = 'vehicules/form.html'
    form_class = VehiculeForm
    success_url = reverse_lazy('vehicules:liste')

class VehiculeUpdateView(UpdateView):
    model = Vehicule
    template_name = 'vehicules/form.html'
    form_class = VehiculeForm
    success_url = reverse_lazy('vehicules:liste')

class DeleteViewVehicule(DeleteView):
    model = Vehicule
    template_name = 'vehicules/confirm_delete.html'
    context_object_name = 'vehicule'
    success_url = reverse_lazy('vehicules:liste')