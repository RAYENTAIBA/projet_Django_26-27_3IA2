from django.urls import path
from .views import *


app_name = 'expeditions'

urlpatterns = [
    path('', ListeViewExpedition.as_view(), name='liste'),
    path('<str:reference>',detail_expedition,name='detail')
]