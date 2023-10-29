from objeto.Clases import *

class ControladorMensajes:
    def __init__(self) -> None:
        self.users = []
        self.hashtags = []
    
    def AgregarUser(self,usuario):
        nuevo = User(usuario)
        self.users.append(nuevo)

    def AgregarHashtag(self,hashtag):
        nuevo = Hashtag(hashtag)
        self.hashtags.append(nuevo)
