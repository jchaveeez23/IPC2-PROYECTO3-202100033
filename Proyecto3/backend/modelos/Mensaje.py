from datetime import datetime
import re
from unicodedata import normalize


class Mensaje:
    def __init__(self, fecha, texto):
        self.fecha = fecha
        self.texto = texto

    def toJSON(self):
        return {
            "fecha": self.fecha,
            "texto": self.texto,
            "hashtags": self.getHashTags(),
            "users": self.getUsers(),
        }

    def getFecha(self):
        fech = self.fecha.split("/")
        fech = datetime(int(fech[2]), int(fech[1]), int(fech[0]))
        return fech

    def getHashTags(self):
        hashtags = [
            i for i in self.texto.split() if i.startswith("#") and i.endswith("#")
        ]
        return list(set(hashtags))

    def getUsers(self):
        users = [i for i in self.texto.split() if i.startswith("@")]
        return list(set(users))

    def getSentimiento(self, sentimientos):
        texto = self.normalizes(self.texto)
        textos = texto.split(" ")
        positivo = 0
        negativo = 0

        for text in textos:
            if text in sentimientos["positivos"]:
                positivo += 1
            elif text in sentimientos["negativos"]:
                negativo += 1

        if positivo > negativo:
            return "positivo"
        elif positivo < negativo:
            return "negativo"
        else:
            return "neutral"

    def normalizes(self, text):
        text = re.sub(
            r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+",
            r"\1",
            normalize("NFD", text),
            0,
            re.I,
        )
        text = normalize("NFC", text)

        return text.lower().strip()
