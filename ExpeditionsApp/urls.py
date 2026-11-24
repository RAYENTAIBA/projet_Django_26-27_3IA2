from django.urls import path
from .views import (
    ListeViewExpedition,
    ExpeditionDetailView,
    ExpeditionCreateView,
    ExpeditionUpdateView,
    ExpeditionDeleteView,
)

app_name = 'expeditions'

urlpatterns = [
    path('', ListeViewExpedition.as_view(), name='liste'),
    path('ajouter/', ExpeditionCreateView.as_view(), name='create'),
    path('<str:reference>/', ExpeditionDetailView.as_view(), name='detail'),
    path('<str:reference>/modifier/', ExpeditionUpdateView.as_view(), name='update'),
    path('<str:reference>/supprimer/', ExpeditionDeleteView.as_view(), name='delete'),
]
