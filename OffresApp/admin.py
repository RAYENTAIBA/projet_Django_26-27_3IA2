from django.contrib import admin
from .models import Offre

# Register your models here.

@admin.register(Offre)
class OffreAdmin(admin.ModelAdmin):
    list_display = ('id', 'prix', 'delai_jours', 'statut', 'expedition', 'transporteur', 'vehicule')
    list_filter = ('statut', 'transporteur', 'date_proposition')
    search_fields = ('expedition__reference', 'transporteur__raison_social', 'vehicule__immmatriculation')
    list_editable = ('statut', 'prix')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 10
