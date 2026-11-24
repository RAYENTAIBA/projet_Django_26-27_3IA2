from django.contrib import admin
from django.urls import path, include
from .views import home, homeWithName
from EntrepriseApp.views import InscriptionView

urlpatterns = [
    path("", home, name='homepage'),
    path('comptes/inscription/', InscriptionView.as_view(), name='inscription'),
    path('comptes/', include('django.contrib.auth.urls')),
    path("home/<str:nom>/", homeWithName, name='home_with_name'),
    path('admin/', admin.site.urls),
    path('expeditions/', include("ExpeditionsApp.urls")),
    path('vehicules/', include("VehiculesApp.urls")),
    path('entreprises/', include("EntrepriseApp.urls")),
    path('offres/', include("OffresApp.urls")),
]
