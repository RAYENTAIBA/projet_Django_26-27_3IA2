import csv
from django.http import HttpResponse
from django.utils.html import format_html
from django.contrib import admin
from .models import Offre


# Register your models here.

@admin.action(description="Exporter la sélection en CSV")
def exporter_offres_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="offres.csv"'
    response.write('\ufeff')  # BOM UTF-8 pour ouverture correcte dans Excel
    writer = csv.writer(response)
    writer.writerow(['reference_expedition', 'transporteur', 'prix', 'statut'])
    for offre in queryset.select_related('expedition', 'transporteur'):
        writer.writerow([
            offre.expedition.reference if offre.expedition else '', 
            offre.transporteur.raison_social if offre.transporteur else '',  # attention : raison_social sans 'e'
            offre.prix, 
            offre.statut
        ])
    return response
    
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
    actions = [exporter_offres_csv]
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
    #new
    def get_readonly_fields(self, request, obj=None):
        base = list(self.readonly_fields)
        if obj and obj.statut == 'acceptee':
            return base + ['prix', 'delai_jours']
        return base


class OffreInline(admin.StackedInline):
    model = Offre
    extra = 0
    fk_name = 'expedition'
    readonly_fields = ('transporteur', 'vehicule', 'prix', 'delai_jours', 'statut')
    show_change_link = True
    can_delete = False

