from django.contrib import admin
from .models import Vehicule

# Register your models here.

@admin.register(Vehicule)
#class VehiculeAdmin(admin.ModelAdmin):
#    list_display = ('immmatriculation', 'type_vehicule', 'capacite_kg', 'disponible', 'entreprise')
 #   list_filter = ('type_vehicule', 'disponible', 'entreprise')
#    search_fields = ('immmatriculation', 'type_vehicule', 'entreprise__raison_social')
#    list_editable = ('disponible', 'capacite_kg')
#    ordering = ('-created_at',)
#    date_hierarchy = 'created_at'
 #   list_per_page = 10

class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('id', 'immmatriculation', 'type_vehicule')
    fieldsets = (
        ("Informations generales", {
            'fields': ('immmatriculation', 'type_vehicule')
        }),
        ("Capacite et caractéristiques", {
            'fields': ('capacite_kg',)
        }),
        ('disponibilite', {
            'fields': ('disponible',)
        }),
        ('transporteur', {
            'fields': ('entreprise',)
        })
    )
    readonly_fields = ('created_at', 'updated_at')

    
