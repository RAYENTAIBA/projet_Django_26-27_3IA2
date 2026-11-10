from django.urls import path
from .views import VehiculeListView, VehiculeCreateView, VehiculeUpdateView, DeleteViewVehicule

app_name = 'vehicules'
urlpatterns = [
    path('', VehiculeListView.as_view(), name='liste'),
    path('create/', VehiculeCreateView.as_view(), name='create'),
    path('<int:pk>/update/', VehiculeUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', DeleteViewVehicule.as_view(), name='delete'),
]