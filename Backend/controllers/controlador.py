from objeto.Clases import *
from controllers.controlador_palabras import *
import xml.etree.ElementTree as ET
import re


class Controlador:
    def __init__(self) -> None:
        self.configuracion = []
        self.mensajes = []
    
    def AgregarConfiguracion(self,palabras_positivas,palabras_negativas):
        nuevo = Configuracion(palabras_positivas,palabras_negativas)
        self.configuracion.append(nuevo)

    def AgregarMensaje(self,fecha,texto,user,hashtag):
        nuevo = Hashtag(fecha,texto,user,hashtag)
        self.mensajes.append(nuevo)

    def LlenarConfiguracion(self,data):
        if data != None:
            root = ET.fromstring(data)
            palabrasbonitas = root.find('PalabrasBonitas')
            if palabrasbonitas is not None:
                cp = ControladorPalabras()
                for palabra in palabrasbonitas.findall('Palabra'):
                    cp.AgregarPalabras(palabra.text)
            
            palabrasfeas = root.find('PalabrasFeas')
            if palabrasfeas is not None:
                cp2 = ControladorPalabras()
                for palabra in palabrasfeas.findall('Palabra'):
                    cp.AgregarPalabras(palabra.text)
                    self.AgregarConfiguracion(cp,cp2)
                return ('Confi hecha')

    def LlenarMensaje(self,data):
        if data != None:
            root = ET.fromstring(data)
            for mensaje in root.findall('MENSAJE'):
                fecha = mensaje.find('FECHA').text
                texto = mensaje.find('TEXTO').text
                usuario = re.findall(r'@(\w+)',texto)
                hashtag = re.findall(r'#(\w+)',texto)
                self.AgregarMensaje(fecha,texto,usuario,hashtag)
            return ('Mensaje hecho')

    @staticmethod
    def convertir(obj):
        return {
            'palabrasbonitas': obj.sentimientos_positivos,
            'palabrasfeas': obj.sentimientos_negativos,

        }
    
    def imprimir(self):
        for mensaje in self.configuracion:
           palabras = mensaje.sentimientos_positivos.palabras
           for palabra in palabras:
               print(palabra)

    def MostrarConfiguracion(self):
        temp_configuracion = []
        for mensaje in self.configuracion:
            temp_configuracion.append(self.convertir(mensaje))

        return ('Configuracion',temp_configuracion)
                    

    