from operator import pos
from turtle import position
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from xml.etree import ElementTree as ET
import re
from unicodedata import normalize
from modelos.Mensaje import Mensaje
from datetime import datetime

app = Flask(__name__)
app.config["DEBUG"] = True

CORS(app)

configurations = {"positivos": [], "negativos": []}
mensajes = []
mensajesFechas = []

@app.route("/cargar/configuracion", methods=["POST"])
def cargarConfiguracion():
    if request.method == "POST":
        file = request.files["file"]
        tree = ET.parse(file)
        diccionario = tree.getroot()
        positivos = diccionario.find("sentimientos_positivos")
        negativos = diccionario.find("sentimientos_negativos")

        for palabra in positivos:
            text = normalizes(palabra.text)
            print(text)
            configurations["positivos"].append(text)

        for palabra in negativos:
            text = normalizes(palabra.text)
            print(text)
            configurations["negativos"].append(text)

        guardarConfiguracionXML()
    return jsonify({"status": "ok"})


@app.route("/cargar/mensajes", methods=["POST"])
def cargarMensajes():
    if request.method == "POST":
        file = request.files["file"]
        tree = ET.parse(file)
        root = tree.getroot()

        threemensajes = root.findall("MENSAJE")
        for mensaje in threemensajes:
            fecha = mensaje.find("FECHA").text
            texto = mensaje.find("TEXTO").text
            fecha = fecha.replace(" ", "")

            if not fecha in mensajesFechas:
                mensajesFechas.append(fecha)

            mensajes.append(Mensaje(fecha, texto))

        guardarMensajesXML()
    return jsonify({"status": "ok"})


@app.route("/data/limpiar", methods=["GET"])
def dataLimpiar():
    configurations = {"positivos": [], "negativos": []}
    mensajes = []
    mensajesFechas = []

    return jsonify({"status": "ok"}), 200


@app.route("/reportes", methods=["GET"])
def reportes():
    dateinicio = request.args.get("dateinicio")
    datefinal = request.args.get("datefinal")
    tiporeporte = request.args.get("tiporeporte")
    if tiporeporte == "1" or tiporeporte == "2":
        hashtagstodos = {}
        dateinicio = parserFecha(dateinicio)
        datefinal = parserFecha(datefinal)
        for mensaje in mensajes:
            fecha = mensaje.getFecha()
            if fecha >= dateinicio and fecha <= datefinal:
                keyfecha = fecha.strftime("%d/%m/%Y")
                if not keyfecha in hashtagstodos:
                    hashtagstodos[keyfecha] = {"fecha": keyfecha, "items": {}}

                if tiporeporte == "1":
                    mensajeItems = mensaje.getHashTags()
                else:
                    mensajeItems = mensaje.getUsers()

                for hashtag in mensajeItems:
                    hashtags = hashtagstodos[keyfecha]["items"]
                    if not hashtag in hashtags:
                        hashtags[hashtag] = 1
                    else:
                        hashtags[hashtag] += 1
        return jsonify({"items": hashtagstodos}), 200

    if tiporeporte == "3":
        dateinicio = parserFecha(dateinicio)
        datefinal = parserFecha(datefinal)
        mensajesFiltrados = {}
        for mensaje in mensajes:
            fecha = mensaje.getFecha()
            if fecha >= dateinicio and fecha <= datefinal:
                keyfecha = fecha.strftime("%d/%m/%Y")
                if not keyfecha in mensajesFiltrados:
                    mensajesFiltrados[keyfecha] = {
                        "fecha": keyfecha,
                        "positivo": 0,
                        "negativo": 0,
                        "neutral": 0,
                    }

                sentimiento = mensaje.getSentimiento(configurations)
                mensajesFiltrados[keyfecha][sentimiento] += 1

        return jsonify({"items": mensajesFiltrados}), 200


def parserFecha(fecha):
    fecha = fecha.split("-")
    fecha = datetime(int(fecha[0]), int(fecha[1]), int(fecha[2]))
    return fecha


def normalizes(text):
    text = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+",
        r"\1",
        normalize("NFD", text),
        0,
        re.I,
    )
    text = normalize("NFC", text)

    return text.lower().strip()


def toJsonArray(array):
    temp = []
    for item in array:
        temp.append(item.toJSON())
    return temp

def guardarConfiguracionXML():
    
    root = ET.Element("CONFIGURACION")
    sumapositivos = len(configurations["positivos"])
    sumanegativos = len(configurations["negativos"])
    positivos = ET.SubElement(root, "PALABRAS_POSITIVAS")
    positivos.text = str(sumapositivos)
    negativos = ET.SubElement(root, "PALABRAS_NEGATIVAS")
    negativos.text = str(sumanegativos)  
    
    tree = ET.ElementTree(root)
    tree.write("resumenConfig.xml")

def guardarMensajesXML():
    root = ET.Element("MENSAJES_RECIBIDOS")
    mensajesfecha = {}

    for mensaje in mensajes:
        fecha = mensaje.getFecha()
        keyfecha = fecha.strftime("%d/%m/%Y")
        if not keyfecha in mensajesfecha:
            mensajesfecha[keyfecha] = {
                "fecha": keyfecha,
                "recibidos": 0,
                "users": 0,
                "hashtags": 0,
            }

        mensajesfecha[keyfecha]["recibidos"] += 1
        mensajesfecha[keyfecha]["users"] += len(mensaje.getUsers())
        mensajesfecha[keyfecha]["hashtags"] += len(mensaje.getHashTags())

        for key in mensajesfecha:
            tiempo = ET.SubElement(root, "TIEMPO")
            fecha = ET.SubElement(tiempo, "FECHA")
            fecha.text = key
            recibidos = ET.SubElement(tiempo, "MSJ_RECIBIDOS")
            recibidos.text = str(mensajesfecha[key]["recibidos"])
            mencionados = ET.SubElement(tiempo, "USR_MENCIONADOS")
            mencionados.text = str(mensajesfecha[key]["users"])
            hashtags = ET.SubElement(tiempo, "HASH_INCLUIDOS")
            hashtags.text = str(mensajesfecha[key]["hashtags"])


    tree = ET.ElementTree(root)
    tree.write("resumenMensajes.xml")
if __name__ == "__main__":
    app.run(debug=True, port=5000)
