from django.shortcuts import render,redirect
import requests
import xml.etree.ElementTree as ET

# Create your views here.
def index(request):
    return render(request, 'index.html')

def cargar_archivo(request):
    return render(request, 'cargar_archivo.html')

def procesar_carga_archivo(request):
    if request.method == 'POST':
        archivo = request.FILES['archivo']
        if archivo:
            files = {'file': archivo}
            url = 'http://localhost:5000/cargar_mensajes'  # La URL de tu servicio Flask
            response = requests.post(url, files=files)
            if response.status_code == 200:
                return redirect('index')  # Redirige a la página de inicio
            else:
                return render(request, 'error.html', {'mensaje': 'Error al cargar el archivo'})
    return render(request, 'cargar_archivo.html')

def cargar_configuracion(request):
    return render(request, 'cargar_configuracion.html')

def procesar_carga_configuracion(request):
    if request.method == 'POST':
        archivo = request.FILES['archivo']
        if archivo:
            files = {'file': archivo}
            url = 'http://localhost:5000/cargar_configuracion'  # La URL de tu servicio Flask
            response = requests.post(url, files=files)
            if response.status_code == 200:
                return redirect('index')  # Redirige a la página de inicio
            else:
                return render(request, 'error.html', {'mensaje': 'Error al cargar el archivo de configuración'})
    return render(request, 'cargar_configuracion.html')

def consultar(request):
    return render(request, 'consultar.html')

def procesar_consulta(request):
    if request.method == 'POST':
        fecha_inicio = request.POST['fecha_inicio']
        fecha_fin = request.POST['fecha_fin']
        url = 'http://localhost:5000/consultar_hashtags'  # La URL de tu servicio Flask
        response = requests.get(url, params={'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin})
        if response.status_code == 200:
            data = parse_response(response.text)
            return render(request, 'resultado_consulta.html', {'data': data})
        else:
            return render(request, 'error.html', {'mensaje': 'Error al consultar datos'})
    return render(request, 'consultar.html')

def parse_response(xml_data):
    data = []
    root = ET.fromstring(xml_data)

    for tiempo in root.findall('TIEMPO'):
        fecha = tiempo.find('FECHA').text
        msj_recibidos = tiempo.find('MSJ_RECIBIDOS').text
        usr_mencionados = tiempo.find('USR_MENCIONADOS').text
        hash_incluidos = tiempo.find('HASH_INCLUIDOS').text

        data.append({
            'fecha': fecha,
            'msj_recibidos': msj_recibidos,
            'usr_mencionados': usr_mencionados,
            'hash_incluidos': hash_incluidos,
        })

    return data