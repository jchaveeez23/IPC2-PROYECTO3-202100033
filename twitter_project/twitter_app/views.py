from django.shortcuts import render
from .forms import FormularioDiccionario
from django.http import HttpResponseRedirect

import requests
import json

# Create your views here.
def PrimeraPagina(request):
    if request.method == 'POST':
        form = FormularioDiccionario(request.POST, request.FILES)
        if form.is_valid():
            contenido = request.FILES['archivo'].read().decode('utf-8')
            print("el contenido es"+contenido)
            url = "http://127.0.0.1:5000/post-archivo-conf"
            Data = {
                "Diccionario" : contenido
            }
            Headers = {'Content-type': 'application/json'}
            data = requests.post(url, json=Data, headers=Headers)
            Datos = data.json()
            print(data.json())
        formulario = FormularioDiccionario()
        return render(request, 'index.html', {'formu': formulario})
    else:
        formulario = FormularioDiccionario()
        return render(request, 'index.html', {'formu': formulario})
    
def SegundaPagina(request):
    return render(request, 'info.html', {})

def PaginaForm_Diccionario(request):
    if request.method == 'POST':
        form = FormularioDiccionario(request.POST,request.FILES)
        if form.is_valid():
            contenido = request.FILES['archivo'].read().decode('utf-8')
            print(contenido)
            url = "http://127.0.0.1:5000/post-archivo-conf"
            Data = {
                "Diccionario" : contenido
            }
            Headers = {'Content-type': 'application/json'}
            data = requests.post(url, json=Data, headers=Headers)
            Datos = data.json()
            print(data.json())
        return render(request, 'Proyecto/Resultado-Form.html', {'Resultado': Datos})
    else:
        formulario = FormularioDiccionario()
        return render(request, 'Formularios/Diccionario.html', {'formu': formulario})
    
def Pagina_GetDiccionario(request):
    url = "http://127.0.0.1:5000/get-palabras"
    data = requests.get(url)
    print(data.json())
    Datos = data.json()
    return render(request, 'Proyecto/Pagina-palabras.html', {'Resultado': Datos})
