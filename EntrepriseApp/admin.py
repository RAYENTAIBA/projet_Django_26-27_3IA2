from django.contrib import admin
from .models import Entreprise
from .models import Utilisateur
from django.contrib.auth.admin import UserAdmin

# Register your models here.

@admin.register(Utilisateur)
class Utilisateur_Admin(UserAdmin):
    list_display = ('user_id', 'username', 'role', 'first_name', 'last_name')
    list_filter = ('user_id', 'created_at')
    search_fields = ('telephone',)
    list_editable = ('role', 'first_name', 'last_name')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 10
    

#admin.site.register(Entreprise)
@admin.register(Entreprise)
class Entreprise_Admin(admin.ModelAdmin):
    list_display = ('raison_social', 'matricule_fiscal', 'type_entreprise', 'adresse', 'gerant')
    list_filter = ('raison_social', 'matricule_fiscal', 'type_entreprise')
    search_fields = ('raison_social', 'matricule_fiscal', 'adresse', 'gerant__username')
    list_editable = ('type_entreprise', 'adresse')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 10

    