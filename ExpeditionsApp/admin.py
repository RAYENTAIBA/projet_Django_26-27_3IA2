from django.contrib import admin, messages
from .models import Expedition
from django.utils import timezone
from django.core.exceptions import ValidationError

# Register your models here.


#class ExpeditionAdmin(admin.ModelAdmin):
#    list_display = ('reference', 'ville_depart', 'ville_arrivee', 'poids_kg', 'statut', 'date_souhaite', 'entreprise')
#    list_filter = ('statut', 'ville_depart', 'ville_arrivee', 'entreprise')
#    search_fields = ('reference', 'ville_depart', 'ville_arrivee', 'entreprise__raison_social')
#    list_editable = ('statut',)
#    ordering = ('-created_at',)
#    date_hierarchy = 'date_souhaite'
#    list_per_page = 10
class EnRetard(admin.SimpleListFilter):
    title = 'en_retard'
    parameter_name = 'en_retard'

    def lookups(self, request, model_admin):
        return [('oui','oui'), ('non','non')]

    def queryset(self, request, queryset):
        if self.value() == 'oui':
            return queryset.filter(statut='publiee',
            date_souhaitee__lt=timezone.now().date())
        if self.value() == 'non':
            return queryset.exclude(statut='publiee',
            date_souhaitee__lt=timezone.now().date())
        return queryset
@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):
    list_display = ('statut',)
    list_filter = [EnRetard]
    fieldsets = (
        ("Informations generales", {
            'fields': ( 'entreprise',)
        }),
        ("Dates et horaires", {
            'fields': ('date_souhaite',)
        }),
        ("Contenu", {
            'fields': ('poids_kg',)
        }),
        ('localisation', {
            'fields': ('ville_depart', 'ville_arrivee')
        }),
        ('statut', {
            'fields': ('statut',)
        })
    )
    readonly_fields = ('created_at', 'updated_at')

    @admin.action(description="cloturer les expeditions selectionnees ")
    def make_it_livree(self,request,queryset):
        liste=queryset.filter(statut='en_cours')
        liste_ignored_nbr=queryset.exclude(statut='en_cours').count()
        compteur=0
        errors=[]
        for ex in liste:
            ex.statut='livree'
            try:
                ex.save()
            except ValidationError as error:
                errors.append(f"L'expedition {ex.reference} erreur lors de modification status : {error.messages}")
        if compteur: 
            self.message_user(request,"expeditions ont ete cloturer", messages.SUCCESS)
        if liste_ignored_nbr :
            self.message_user(request, "expeditions ignores", messages.WARNING)
        for e in errors:
            self.message_user(request, e, messages.ERROR)
    actions = [make_it_livree]



