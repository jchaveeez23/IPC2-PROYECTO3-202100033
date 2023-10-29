from django.urls import path
from . import views

urlpatterns = [
    path('inicio/', views.PrimeraPagina, name="PrimeraPagina"),
    path('inicio/info/', views.SegundaPagina, name="SegundaPagina"),
    path('Form-Diccionario/', views.PaginaForm_Diccionario, name='Form Diccionario'),
    path('Diccionario/', views.Pagina_GetDiccionario, name="Pagina de palabras"),

]