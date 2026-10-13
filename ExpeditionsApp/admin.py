from django.contrib import admin
from .models import Expedition

# Register your models here.

@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):
    list_display = ('reference', 'ville_depart', 'ville_arrivee', 'poids_kg', 'statut', 'date_souhaite', 'entreprise')
    list_filter = ('statut', 'ville_depart', 'ville_arrivee', 'entreprise')
    search_fields = ('reference', 'ville_depart', 'ville_arrivee', 'entreprise__raison_social')
    list_editable = ('statut',)
    ordering = ('-created_at',)
    date_hierarchy = 'date_souhaite'
    list_per_page = 10
