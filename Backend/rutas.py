from flask import Flask, request, jsonify, make_response
import xml.etree.ElementTree as ET
from collections import defaultdict
import datetime
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO

app = Flask(__name__)

# Variables globales para almacenar datos
mensajes = []
configuracion = {'positivos': set(), 'negativos': set()}
resultados = []

# Rutas para cargar archivos XML y procesar datos
@app.route('/cargar_mensajes', methods=['POST'])
def cargar_mensajes():
    global mensajes
    uploaded_file = request.files['file']  # Obtener el archivo XML de la solicitud
    if uploaded_file:
        tree = ET.ElementTree(ET.fromstring(uploaded_file.read()))
        for mensaje_xml in tree.findall(".//MENSAJE"):
            fecha = mensaje_xml.find("FECHA").text
            texto = mensaje_xml.find("TEXTO").text
            mensajes.append({'fecha': fecha, 'texto': texto})
        return 'Mensajes cargados exitosamente'
    return 'Error al cargar mensajes'

@app.route('/cargar_configuracion', methods=['POST'])
def cargar_configuracion():
    global configuracion
    uploaded_file = request.files['file']  # Obtener el archivo XML de configuración
    if uploaded_file:
        tree = ET.ElementTree(ET.fromstring(uploaded_file.read()))
        for palabra in tree.findall(".//palabra"):
            configuracion['positivos'].add(palabra.text.lower())
        for palabra in tree.findall(".//sentimientos_negativos/palabra"):
            configuracion['negativos'].add(palabra.text.lower())
        return 'Configuración cargada exitosamente'
    return 'Error al cargar configuración'

# Lógica para procesar mensajes y calcular sentimientos
def procesar_mensajes():
    global mensajes
    global configuracion
    global resultados

    fecha_actual = None
    sentimientos = defaultdict(int)
    usuarios_mencionados = set()
    hashtags_incluidos = set()

    for mensaje in mensajes:
        fecha, texto = mensaje['fecha'], mensaje['texto']
        fecha_actual = datetime.datetime.strptime(fecha, "%B %d, %Y %H:%M hrs.")
        # Resto de la lógica para analizar el texto y calcular sentimientos, usuarios y hashtags
        palabras = texto.split()
        for palabra in palabras:
            palabra = palabra.lower()  # Convertir a minúsculas
            if palabra.startswith('@'):
                usuarios_mencionados.add(palabra[1:])
            elif palabra.startswith('#'):
                hashtags_incluidos.add(palabra[1:])
            elif palabra in configuracion['positivos']:
                sentimientos['positivos'] += 1
            elif palabra in configuracion['negativos']:
                sentimientos['negativos'] += 1

    # Calcular resultados y almacenarlos en la lista de resultados
    resultado = {
        'fecha': fecha_actual.strftime('%d/%m/%Y'),
        'mensajes_recibidos': len(mensajes),
        'usuarios_mencionados': len(usuarios_mencionados),
        'hashtags_incluidos': len(hashtags_incluidos),
        'sentimientos_positivos': sentimientos['positivos'],
        'sentimientos_negativos': sentimientos['negativos']
    }
    resultados.append(resultado)

# Generar archivo XML de salida con los resultados
def generar_reporte_xml():
    root = ET.Element('MENSAJES_RECIBIDOS')
    for resultado in resultados:
        tiempo = ET.SubElement(root, 'TIEMPO')
        fecha = ET.SubElement(tiempo, 'FECHA')
        fecha.text = resultado['fecha']
        mensajes_recibidos = ET.SubElement(tiempo, 'MSJ_RECIBIDOS')
        mensajes_recibidos.text = str(resultado['mensajes_recibidos'])
        usuarios_mencionados = ET.SubElement(tiempo, 'USR_MENCIONADOS')
        usuarios_mencionados.text = str(resultado['usuarios_mencionados'])
        hashtags_incluidos = ET.SubElement(tiempo, 'HASH_INCLUIDOS')
        hashtags_incluidos.text = str(resultado['hashtags_incluidos'])

    tree = ET.ElementTree(root)
    tree.write('resumenMensajes.xml')

# Rutas para consultar hashtags, menciones y sentimientos
@app.route('/consultar_hashtags', methods=['GET'])
def consultar_hashtags():
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    resultados_filtrados = [resultado for resultado in resultados if fecha_inicio <= resultado['fecha'] <= fecha_fin]
    hashtags = defaultdict(int)
    for resultado in resultados_filtrados:
        for hashtag in resultado['hashtags_incluidos']:
            hashtags[hashtag] += 1
    sorted_hashtags = dict(sorted(hashtags.items(), key=lambda item: item[1], reverse=True))
    return jsonify(sorted_hashtags)

@app.route('/consultar_menciones', methods=['GET'])
def consultar_menciones():
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    resultados_filtrados = [resultado for resultado in resultados if fecha_inicio <= resultado['fecha'] <= fecha_fin]
    usuarios = defaultdict(int)
    for resultado in resultados_filtrados:
        for usuario in resultado['usuarios_mencionados']:
            usuarios[usuario] += 1
    sorted_usuarios = dict(sorted(usuarios.items(), key=lambda item: item[1], reverse=True))
    return jsonify(sorted_usuarios)

@app.route('/consultar_sentimientos', methods=['GET'])
def consultar_sentimientos():
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    resultados_filtrados = [resultado for resultado in resultados if fecha_inicio <= resultado['fecha'] <= fecha_fin]
    positivos = 0
    negativos = 0
    neutros = 0
    for resultado in resultados_filtrados:
        if resultado['sentimientos_positivos'] > resultado['sentimientos_negativos']:
            positivos += 1
        elif resultado['sentimientos_positivos'] < resultado['sentimientos_negativos']:
            negativos += 1
        else:
            neutros += 1
    return jsonify({'positivos': positivos, 'negativos': negativos, 'neutros': neutros})


# Generar informes en formato PDF
def generar_pdf(data, filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []

    # Insertar datos en una tabla
    data.insert(0, ['Palabra', 'Frecuencia'])  # Encabezados
    t = Table(data)

    # Estilo de la tabla
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    t.setStyle(style)

    elements.append(t)

    # Construir el PDF
    doc.build(elements)

# Uso de la función para generar un PDF a partir de datos tabulares
data = [['Palabra1', 10], ['Palabra2', 20], ['Palabra3', 15]]
generar_pdf(data, 'informe.pdf')
