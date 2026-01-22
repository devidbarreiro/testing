from django.urls import path
from .views import generar_pildora

urlpatterns = [
    path('', generar_pildora, name='home'),
    path('api/generar', generar_pildora, name='api_generar'),
]