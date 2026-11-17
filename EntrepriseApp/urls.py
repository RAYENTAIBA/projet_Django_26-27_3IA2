from django.urls import path
from .views import (
    EntrepriseListView,
    EntrepriseDetailView,
    EntrepriseCreateView,
    EntrepriseUpdateView,
    EntrepriseDeleteView,
)

app_name = 'entreprises'

urlpatterns = [
    path('', EntrepriseListView.as_view(), name='liste'),
    path('<int:pk>/', EntrepriseDetailView.as_view(), name='detail'),
    path('create/', EntrepriseCreateView.as_view(), name='create'),
    path('<int:pk>/update/', EntrepriseUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', EntrepriseDeleteView.as_view(), name='delete'),
]
