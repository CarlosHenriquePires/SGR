from django.forms import ModelForm,forms
from appsgr.models import *

class RequerimentoForm(ModelForm):
    class Meta:
        model=Requerimento
        fields=('__all__')
