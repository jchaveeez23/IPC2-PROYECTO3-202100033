from django import forms

class FormularioDiccionario(forms.Form):
    archivo = forms.FileField()
