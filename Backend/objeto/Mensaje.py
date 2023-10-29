import xml.etree.ElementTree as ET

class Mensajes:
    def __init__(self):
        self.ListaMensajes = []
        self.Fecha = []
        self.Texto = []
        self.ListaHashtag = []
        self.Hashtag = []
        self.ListaMenciones = []
        self.Menciones = []
        self.ListaMensajes = []
        direccion = "BaseDatos/Mensajes.xml"
        ArchivoXML = ET.parse(direccion)
        Raiz = ArchivoXML.getroot()
        self.CargarMensaje(Raiz)

    def CargarMensaje(self, ArbolXML):
        for Categoria in ArbolXML:
            if Categoria.tag == "Mensaje":
                print(Categoria)
                self.ListaMensajes.append(Categoria.text)

                for Mensaje in Categoria:
                    self.ListaMensajes.append(Mensaje.text)
                    if Mensaje.tag =="Fecha":
                        print(Mensaje)
                        self.Fecha.append(Mensaje.text)
                        print(self.Fecha,"Es la FECHAAAAAAAA")
                    if Mensaje.tag =="Texto":
                        print(Mensaje)
                        self.Texto.append(Mensaje.text)
                        print(self.Texto,"Es el TEXTOOOOO")
                    if Mensaje.tag =="ListaHashtag":
                        print(Mensaje)
                        self.ListaHashtag.append(Mensaje.text)
                        for ListaHash in Mensaje:
                            if ListaHash.tag =="Hashtag":
                                print(ListaHash)
                                self.Hashtag.append(ListaHash.text)
                                print(self.Hashtag,"Es el HASHTAG")
                                
                    if Mensaje.tag =="ListaMenciones":
                        print(Mensaje)
                        for ListaMenciones in Mensaje:
                            if ListaMenciones.tag =="Menciones":
                                print(ListaMenciones)
                                self.Menciones.append(ListaMenciones.text)
                                print(self.Menciones,"Es la MENCION")



    def CargarNuevosMensajes(self, ArbolXML):
        for Los_Mensajes in ArbolXML:
            if Los_Mensajes.tag == "Mensaje":
                print(Los_Mensajes)
                self.ListaMensajes.append(Los_Mensajes.text)

                for Mensaje in Los_Mensajes:
                    self.ListaMensajes.append(Mensaje.text)
                    if Mensaje.tag =="Fecha":
                        print(Mensaje)
                        self.Fecha.append(Mensaje.text)
                        print(self.Fecha,"Es la FECHAAAAAAAA")
                    if Mensaje.tag =="Texto":
                        print(Mensaje)
                        self.Texto.append(Mensaje.text)
                        print(self.Texto,"Es el TEXTOOOOO")
                    if Mensaje.tag =="ListaHashtag":
                        print(Mensaje)
                        self.ListaHashtag.append(Mensaje.text)
                        # print(self.ListaHashtag,"Es la LISTADEHASHTAG")
                        for ListaHash in Mensaje:
                            if ListaHash.tag =="Hashtag":
                                print(ListaHash)
                                self.Hashtag.append(ListaHash.text)
                                print(self.Hashtag,"Es el HASHTAG")
                                
                    if Mensaje.tag =="ListaMenciones":
                        print(Mensaje)
                        for ListaMenciones in Mensaje:
                            if ListaMenciones.tag =="Menciones":
                                print(ListaMenciones)
                                self.Menciones.append(ListaMenciones.text)
                                print(self.Menciones,"Es la MENCION")
        self.OrdenarPalabras()

        #Necesita un analisis mas profundo, es decir que no se repitan palabras

    def GuardarMensaje(self):
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

    def ObtenerMensajesJson(self):
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