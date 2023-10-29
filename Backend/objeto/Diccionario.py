import xml.etree.ElementTree as ET


class Diccionario:
    def __init__(self):
        self.PalabrasPositivas = []
        self.PalabrasNegativas = []
        direccion = "BaseDatos/Diccionario.xml"
        ArchivoXML = ET.parse(direccion)
        Raiz = ArchivoXML.getroot()
        self.CargarDiccionario(Raiz)        

    def CargarDiccionario(self, ArbolXML):
        for Categoria in ArbolXML:
            if Categoria.tag == "PalabrasBonitas":
                for Palabra in Categoria:
                    self.PalabrasPositivas.append(Palabra.text)
            if Categoria.tag == "PalabrasFeas":
                for Palabra in Categoria:
                    self.PalabrasNegativas.append(Palabra.text)

    def CargarNuevasPalabras(self, ArbolXML):
        for Sentimientos in ArbolXML:
            if Sentimientos.tag == "sentimientos_positivos":
                for Palabra in Sentimientos:
                    self.PalabrasPositivas.append(Palabra.text)

            if Sentimientos.tag == "sentimientos_negativos":
                for Palabra in Sentimientos:
                    self.PalabrasNegativas.append(Palabra.text)
        self.OrdenarPalabras()

        #Necesita un analisis mas profundo, es decir que no se repitan palabras

    def GuardarDiccionario(self):
        RaizDiccionario = ET.Element("Diccionario")
        PalabrasBonitas = ET.SubElement(RaizDiccionario, "PalabrasBonitas")
        PalabrasFeas = ET.SubElement(RaizDiccionario, "PalabrasFeas")
        for Palabra in self.PalabrasPositivas:
            TagPalabra = ET.SubElement(PalabrasBonitas, "Palabra")
            TagPalabra.text = Palabra

        for Palabra in self.PalabrasNegativas:
            TagPalabra = ET.SubElement(PalabrasFeas, "Palabra")
            TagPalabra.text = Palabra
        Arbol = ET.ElementTree(RaizDiccionario)
        ET.indent(Arbol, space="\t", level=0)
        Arbol.write("BaseDatos/Diccionario.xml", encoding="utf-8")

    def ObtenerPalabrasJson(self):
        SalidaJson = {
            "PalabrasPositivas": [],
            "PalabrasNegativas": []
        }
        for Palabra in self.PalabrasPositivas:
            SalidaJson["PalabrasPositivas"].append(Palabra)

        for Palabra in self.PalabrasNegativas:
            SalidaJson["PalabrasNegativas"].append(Palabra)

        return SalidaJson
    
    def OrdenarPalabras(self):
        print("ordenando")

    def Reiniciar(self):
        RaizDiccionario = ET.Element("Diccionario")
        PalabrasBonitas = ET.SubElement(RaizDiccionario, "PalabrasBonitas")
        PalabrasFeas = ET.SubElement(RaizDiccionario, "PalabrasFeas")
        Arbol = ET.ElementTree(RaizDiccionario)
        ET.indent(Arbol, space="\t", level=0)
        Arbol.write("BaseDatos/Diccionario.xml", encoding="utf-8")