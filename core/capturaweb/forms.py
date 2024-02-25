from django import forms

from core.capturaweb.models import Grabacion, GrabacionProgramada

FORMATO = ((1, "AUDIO-VIDEO"), (2, "AUDIO"))


class DatosGrabacionForm(forms.ModelForm):
    TIPO = ((1, "CONTINUA"), (2, "SEGMENTADA"))
    CONVERTIR = ((True, "SI"), (False, "NO"))

    tipo_grabacion = forms.ChoiceField(choices=TIPO, initial='1',
                                       widget=forms.RadioSelect(attrs={'class': 'btn-check'}))
    convertida = forms.ChoiceField(choices=CONVERTIR, initial=False,
                                   widget=forms.RadioSelect(attrs={'class': 'btn-check'}))
    segmento = forms.CharField(max_length=4, initial=10, required=False,
                               widget=forms.TextInput(attrs={'style': 'visibility: hidden;'}))

    class Meta:
        model = Grabacion
        fields = ['titulo', 'convertida', 'tipo_grabacion']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ProgramarGrabacionForm(forms.ModelForm):
    TIPO = ((1, "CONTINUA"), (2, "SEGMENTADA"))
    CONVERTIR = ((True, "SI"), (False, "NO"))

    tipo_grabacion = forms.ChoiceField(choices=TIPO, initial='1',
                                       widget=forms.RadioSelect(attrs={'class': 'btn-check'}))
    convertida = forms.ChoiceField(choices=CONVERTIR, initial=False,
                                   widget=forms.RadioSelect(attrs={'class': 'btn-check'}))
    segmento = forms.CharField(max_length=4, initial=60, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'visibility: hidden;'}))

    class Meta:
        model = GrabacionProgramada
        fields = ['titulo', 'hora_inicio', 'hora_fin', 'lunes', 'martes', 'miercoles', 'jueves', 'viernes',
                  'sabado', 'domingo', 'convertida', 'tipo_grabacion']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            # 'fecha': forms.DateInput(
            #     format='%Y-%m-%d',
            #     attrs={'class': 'form-control',
            #            'type': 'date'
            #            }),
            'hora_inicio': forms.TimeInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'time'
                       }),
            'hora_fin': forms.TimeInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'time'
                       }),
            'lunes': forms.CheckboxInput(
                attrs={'class': 'btn-check',
                       'type': 'checkbox'
                       }),
            'martes': forms.CheckboxInput(
                attrs={'class': 'btn-check',
                       'type': 'checkbox'
                       }),
            'miercoles': forms.CheckboxInput(
                attrs={'class': 'btn-check',
                       'type': 'checkbox'
                       }),
            'jueves': forms.CheckboxInput(
                attrs={'class': 'btn-check',
                       'type': 'checkbox'
                       }),
            'viernes': forms.CheckboxInput(
                attrs={'class': 'btn-check',
                       'type': 'checkbox'
                       }),
            'sabado': forms.CheckboxInput(
                attrs={'class': 'btn-check',
                       'type': 'checkbox'
                       }),
            'domingo': forms.CheckboxInput(
                attrs={'class': 'btn-check',
                       'type': 'checkbox'
                       }),
        }


class DescargaForm(forms.Form):
    url = forms.CharField(label="URL", max_length=200, required=True)
    formato = forms.ChoiceField(widget=forms.RadioSelect, choices=FORMATO, required=True)
