from controllers.controllers import *
from controllers.ControlBaseDatos import *
from flask import Blueprint, jsonify, Response, request

RP  = Blueprint("Rutas",__name__)
# Lista para almacenar los mensajes
mensajes = []

@RP.route("/get-palabras", methods=["GET"])
def ObtenerPalabas():
    Resultado = Get_Palabras()
    return (jsonify(Resultado))

@RP.route("/post-archivo-conf", methods=["POST"])
def Archivo_Conf():
    #print(request.data)
    Resultado = Configuracion_Diccionario(request.data)
    return(jsonify(Resultado))

@RP.route("/CargarDiccionario", methods=["GET"])
def CargaDiccionario():
    Resultado = LeerDiccionario()
    return(Resultado)

@RP.route("/ReiniciarDiccionario", methods=["GET"])
def RoutesReiniciarDiccionario():
    Resultado = ReiniciarDiccioario()
    return Resultado


