from django import forms

TIPO = ((1, "CONTINUA"), (2, "SEGMENTADA"))
CONVERTIR = ((1, "SI"), (2, "NO"))
FORMATO = ((1, "AUDIO-VIDEO"), (2, "AUDIO"))


class DatosGrabacionForm(forms.Form):
    nombre = forms.CharField(max_length=100, required=True)
    tipo_grabacion = forms.ChoiceField(widget=forms.RadioSelect, choices=TIPO, required=True, initial="1")
    segmento = forms.CharField(max_length=4, initial=10, required=False)
    convertir = forms.ChoiceField(widget=forms.RadioSelect, choices=CONVERTIR, required=True, initial="2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['tipo_grabacion'].widget.attrs.update({'class': 'form-control'})
        self.fields['segmento'].widget.attrs.update({'class': 'form-control mt-2', 'id': 'segmento'})
        self.fields['convertir'].widget.attrs.update({'class': 'form-check-input'})


class DescargaForm(forms.Form):
    url = forms.CharField(label="URL", max_length=200, required=True)
    formato = forms.ChoiceField(widget=forms.RadioSelect, choices=FORMATO, required=True)
