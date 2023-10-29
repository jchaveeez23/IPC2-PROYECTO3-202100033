class Configuracion:
    def __init__(self,sentimientos_positivos,sentimientos_negativos) -> None:
        self.sentimientos_positivos = sentimientos_positivos
        self.sentimientos_negativos = sentimientos_negativos

class Palabras_positivas:
    def __init__(self,palabras) -> None:
        self.palabras = palabras

class Palabras_negativas:
    def __init__(self,palabras) -> None:
        self.palabras = palabras

class Mensajes:
    def __init__(self,fecha,texto,user,hashtag) -> None:
       self.fecha = fecha
       self.texto = texto
       self.user = user
       self.hashtag = hashtag

class User:
    def __init__(self,usuarios) -> None:
        self.usuarios = usuarios

class Hashtag:
    def __init__(self,Hashtag) -> None:
        self.Hashtag = Hashtag