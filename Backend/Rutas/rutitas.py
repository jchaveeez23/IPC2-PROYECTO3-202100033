from controllers.controllers import *
from controllers.ControlBaseDatos import *
from controllers.controlador import *
from flask import Blueprint, jsonify, Response, request
control = Controlador()

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

@RP.route("/grabarMensajes",methods =["POST"])
def GrabarMensajes():
    pass

@RP.route("/grabarConfiguracion",methods =["POST"])
def GrabarConfiguracion():
    print(request.data)
    variable = control.LlenarConfiguracion(request.data)
    print(variable)
    control.imprimir()
    return Response(variable,status=201)

@RP.route("/imprimir",methods =["GET"])
def mostrarconfig():
    resp = control.MostrarConfiguracion()
    response = {}
    if (resp != False):
        return jsonify(resp)
    else:
        response = {'messsage':'error xd'},500
        return response
    


