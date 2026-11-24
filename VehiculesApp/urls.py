from django.urls import path
from .views import VehiculeListView, VehiculeCreateView, VehiculeUpdateView, VehiculeDeleteView

app_name = 'vehicules'

urlpatterns = [
    path('', VehiculeListView.as_view(), name='liste'),
    path('create/', VehiculeCreateView.as_view(), name='create'),
    path('ajouter/', VehiculeCreateView.as_view(), name='ajouter'),
    path('<int:pk>/update/', VehiculeUpdateView.as_view(), name='update'),
    path('<int:pk>/modifier/', VehiculeUpdateView.as_view(), name='modifier'),
    path('<int:pk>/delete/', VehiculeDeleteView.as_view(), name='delete'),
    path('<int:pk>/supprimer/', VehiculeDeleteView.as_view(), name='supprimer'),
]
