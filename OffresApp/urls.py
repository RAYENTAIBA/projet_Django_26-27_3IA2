from django.urls import path
from .views import OffreListView, OffreCreateView, OffreDeleteView

app_name = 'offres'

urlpatterns = [
    path('', OffreListView.as_view(), name='liste'),
    path('ajouter/', OffreCreateView.as_view(), name='ajouter'),
    path('<int:pk>/delete/', OffreDeleteView.as_view(), name='delete'),
]
