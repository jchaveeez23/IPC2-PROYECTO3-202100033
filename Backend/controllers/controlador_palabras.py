from objeto.Clases import *

class ControladorPalabras:
    def __init__(self) -> None:
        self.palabras = []

    def AgregarPalabras(self,palabra):
        nuevo = Palabras_positivas(palabra)
        self.palabras.append(nuevo)