from django.utils.html import format_html
from django.contrib import admin
from .models import Offre


# Register your models here.

@admin.register(Offre)
#class OffreAdmin(admin.ModelAdmin):
#    list_display = ('id', 'prix', 'delai_jours', 'statut', 'expedition', 'transporteur', 'vehicule')
#    list_filter = ('statut', 'transporteur', 'date_proposition')
#    search_fields = ('expedition__reference', 'transporteur__raison_social', 'vehicule__immmatriculation')
 #   list_editable = ('statut_colore', 'prix')
#    ordering = ('-created_at',)
#    date_hierarchy = 'created_at'
 #   list_per_page = 10



class OffreAdmin(admin.ModelAdmin):
    list_display = ('id', 'prix', 'statut_colore')
    fieldsets = (
       ("Informations generales", {
           'fields': ('expedition', 'transporteur', 'vehicule')
        }),
        ("Informationsfinancieres", {
            'fields': ('prix','delai_jours')
        }),
        ("statut", {
            'fields': ('statut',)
        })
    )
    readonly_fields = ('created_at', 'updated_at',)
    @admin.display(description='Statut')
    def statut_colore(self, obj):
        couleurs = {
            'proposee': '#F0AD4E', 'acceptee': '#5CB85C',
            'refusee': '#D9534F', 'retiree': '#777777',
        }
        return format_html(
        '<span style="color:white;background:{};padding:3px 8px;border-radius:4px;">{}</span>',
    couleurs.get(obj.statut, '#999'), obj.get_statut_display(),
    )