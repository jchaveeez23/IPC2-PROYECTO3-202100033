from django.shortcuts import render
import requests


def index(request):
    ctx = {"content": None, "response": None, "msg": "", "color": "green"}

    return render(request, "home.html", ctx)


def archivos(request):
    ctx = {"content": None, "response": None, "msg": None, "color": "green"}

    return render(request, "Files.html", ctx)

def datos(request):
    ctx = {"content": None, "response": None, "msg": None, "color": "green"}

    return render(request, "Datos.html", ctx)


def documentacion(request):
    ctx = {"content": None, "response": None, "msg": None, "color": "green"}

    return render(request, "Documentacion.html", ctx)


def cargarConfiguracion(request):
    ctx = {"content": None, "response": None, "msg": None, "color": "green"}
    if request.method == "POST":
        f = request.FILES["file-config"]
        xml_binary = f.read()
        files = {"file": xml_binary}
        response = requests.post(
            "http://127.0.0.1:5000/cargar/configuracion", files=files
        )

        if response.status_code == 200:
            ctx["response"] = response.json()
        else:
            ctx["msg"] = response.json()["msg"]
            ctx["color"] = "red"

    return render(request, "FileSuccess.html", ctx)


def cargarMensajes(request):
    ctx = {"content": None, "response": None, "msg": None, "color": "green"}
    if request.method == "POST":
        f = request.FILES["file-mensajes"]
        xml_binary = f.read()
        files = {"file": xml_binary}
        response = requests.post("http://127.0.0.1:5000/cargar/mensajes", files=files)

        if response.status_code == 200:
            ctx["response"] = response.json()
        else:
            ctx["msg"] = response.json()["msg"]
            ctx["color"] = "red"

    return render(request, "FileSuccess.html", ctx)


def limpiarData(request):
    ctx = {"content": None, "response": None, "msg": None, "color": "green"}
    if request.method == "GET":
        response = requests.get("http://127.0.0.1:5000/data/limpiar")

        if response.status_code == 200:
            ctx["response"] = response.json()
        else:
            ctx["msg"] = response.json()["msg"]
            ctx["color"] = "red"

    return render(request, "Limpieza.html", ctx)


def resultados(request):
    ctx = {"content": None, "tipo": 0, "response": None, "msg": None, "color": "green"}
    if request.method == "POST":
        # get from form, dateinicio, datefinal y tiporeporte from select
        dateinicio = request.POST.get("dateinicio")
        datefinal = request.POST.get("datefinal")
        tiporeporte = request.POST.get("tiporeporte")
        response = requests.get(
            "http://127.0.0.1:5000/reportes"
            + "?dateinicio="
            + dateinicio
            + "&datefinal="
            + datefinal
            + "&tiporeporte="
            + tiporeporte
            ,
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )

        if response.status_code == 200:
            ctx["tipo"] = tiporeporte
            ctx["content"] = response.json()
            print(response.json())

        return render(request, "Resultados.html", ctx)

    if request.method == "GET":
        return render(request, "Resultados.html", ctx)
