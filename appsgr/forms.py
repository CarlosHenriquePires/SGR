from django.forms import ModelForm,forms
from appsgr.models import *

class RequerimentoForm(ModelForm):
    class Meta:
        model=Requerimento
        fields=('__all__')

class RequerimentoFormUpdate(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RequerimentoFormUpdate, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['codigo'].widget.attrs['readonly'] = True
            self.fields['aluno'].widget.attrs['readonly'] = True
            self.fields['tipo_requerimento'].widget.attrs['readonly'] = True
            self.fields['disciplina'].widget.attrs['readonly'] = True
            self.fields['observacoes'].widget.attrs['readonly'] = False
            self.fields['justificativa'].widget.attrs['readonly'] = True
            self.fields['data_atividade'].widget.attrs['readonly'] = True
            self.fields['professor_atividade'].widget.attrs['readonly'] = True
            self.fields['documentos_apresentados'].widget.attrs['readonly'] = True
            self.fields['documentos_files'].widget.attrs['readonly'] = True
            self.fields['tipo_atividade'].widget.attrs['readonly'] = True
            self.fields['encaminhado_para'].widget.attrs['readonly'] = False
            self.fields['situacao'].widget.attrs['readonly'] = False

    def clean_aluno(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.aluno
        else:
            return self.cleaned_data['aluno']

    def clean_tipo_requerimento(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.tipo_requerimento
        else:
            return self.cleaned_data['tipo_requerimento']

    def clean_disciplina(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.disciplina
        else:
            return self.cleaned_data['disciplina']

    def clean_professor_atividade(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.professor_atividade
        else:
            return self.cleaned_data['professor_atividade']

    def clean_documentos_apresentados(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.documentos_apresentados
        else:
            return self.cleaned_data['documentos_apresentados']

    def clean_documentos_files(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.documentos_files
        else:
            return self.cleaned_data['documentos_files']
    class Meta:
        model=Requerimento
        fields=('__all__')
