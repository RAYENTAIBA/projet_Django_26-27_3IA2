from django.contrib import admin
from .models import Entreprise
from .models import Utilisateur
from django.contrib.auth.admin import UserAdmin
admin.site.site_header='TransConnect - Administration'
admin.site.site_title='TransConnect'
admin.site.index_title='Tableau de bord'
# Register your models here.

@admin.register(Utilisateur)
#class Utilisateur_Admin(UserAdmin):
#    list_display = ('user_id', 'username', 'role', 'first_name', 'last_name')
#    list_filter = ('user_id', 'created_at')
#    search_fields = ('telephone',)
#    list_editable = ('role', 'first_name', 'last_name')
#    ordering = ('-created_at',)
#    date_hierarchy = 'created_at'
#    list_per_page = 10

class Utilisateur_Admin(admin.ModelAdmin):
    list_display = ('user_id', 'telephone', 'role')
    fieldsets = (
        ("Identite utilisateur", {
            'fields': ('user_id', 'telephone','email')
        }),
        ("Informations personnelles", {
            'fields': ('first_name', 'last_name', 'password', 'username')
        }),
        ('role', {
            'fields': ('role',)
        })
    )
    readonly_fields = ('created_at', 'updated_at','user_id')
    

#admin.site.register(Entreprise)
@admin.register(Entreprise)
#class Entreprise_Admin(admin.ModelAdmin):
#    list_display = ('raison_social', 'matricule_fiscal', 'type_entreprise', 'adresse', 'gerant')
#    list_filter = ('raison_social', 'matricule_fiscal', 'type_entreprise')
#    search_fields = ('raison_social', 'matricule_fiscal', 'adresse', 'gerant__username')
 #   list_editable = ('type_entreprise', 'adresse')
 #   ordering = ('-created_at',)
 #   date_hierarchy = 'created_at'
#    list_per_page = 10

class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ('raison_social',)
    fieldsets = (
        ("Identite entreprise", {
            'fields': ('raison_social', 'matricule_fiscal','type_entreprise')
        }),
        ("Contact entreprise", {
            'fields': ('adresse', 'gerant')
        }),
        ('date systeme', {
            'fields': ('created_at', 'updated_at')
        })
    )
    readonly_fields = ('created_at', 'updated_at')

    