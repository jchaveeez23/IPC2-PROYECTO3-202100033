from flask import Flask
from Rutas.rutitas import RP

app = Flask(__name__)
app.register_blueprint(RP)