from django import forms

from core.capturaweb.models import Grabacion

FORMATO = ((1, "AUDIO-VIDEO"), (2, "AUDIO"))


class DatosGrabacionForm(forms.ModelForm):
    TIPO = ((1, "CONTINUA"), (2, "SEGMENTADA"))
    CONVERTIR = ((True, "SI"), (False, "NO"))

    tipo_grabacion = forms.ChoiceField(choices=TIPO, initial='1',
                                       widget=forms.RadioSelect(attrs={'class': 'form-check'}))
    convertida = forms.ChoiceField(choices=CONVERTIR, initial=False,
                                   widget=forms.RadioSelect(attrs={'class': 'form-check'}))
    segmento = forms.CharField(max_length=4, initial=10, required=False,
                               widget=forms.TextInput(attrs={'style': 'visibility: hidden;'}))

    class Meta:
        model = Grabacion
        fields = ['titulo', 'convertida', 'tipo_grabacion']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
        }


class DescargaForm(forms.Form):
    url = forms.CharField(label="URL", max_length=200, required=True)
    formato = forms.ChoiceField(widget=forms.RadioSelect, choices=FORMATO, required=True)
