from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Página de inicio
    path('cargar-archivo/', views.cargar_archivo, name='cargar_archivo'),  # Página para cargar archivo XML
    path('procesar-carga-archivo/', views.procesar_carga_archivo, name='procesar_carga_archivo'),  # Procesar carga de archivo XML
    path('cargar-configuracion/', views.cargar_configuracion, name='cargar_configuracion'),  # Página para cargar configuración
    path('procesar-carga-configuracion/', views.procesar_carga_configuracion, name='procesar_carga_configuracion'),  # Procesar carga de configuración
    path('consultar/', views.consultar, name='consultar'),  # Página para realizar consultas
    path('procesar-consulta/', views.procesar_consulta, name='procesar_consulta'),  # Procesar consultas
]