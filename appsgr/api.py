from tastypie.resources import ModelResource
from tastypie import fields
from .models import *
from tastypie.authorization import Authorization

class PessoaResource(ModelResource):
    class Meta:
        queryset = Pessoa.objects.all()
        resource_name='pessoa'
        fields=['username','first_name','last_name']

class ProfessorResource(ModelResource):
    pessoa=fields.ToOneField('appssgr.api.PessoaResource','pessoa',full=True)
    class Meta:
        queryset = Professor.objects.all()
        resource_name='professor'
        fields=['pessoa','first_name','last_name']

class TecAdmResource(ModelResource):
    pessoa=fields.ToOneField('appssgr.api.PessoaResource','pessoa',full=True)
    class Meta:
        queryset = Tecnico_Administrativo.objects.all()
        resource_name='tecadm'

class CursoResource(ModelResource):
    class Meta:
        queryset = Curso.objects.all()
        resource_name='curso'

class DisciplinaResource(ModelResource):
    aluno = fields.ToManyField('appssgr.api.AlunoResource', 'aluno',full=True)
    curso = fields.ToManyField('appssgr.api.CursoResource','curso',full=True)
    always_return_data = True
    class Meta:
        queryset = Disciplina.objects.all()
        resource_name = 'disciplina'

class AlunoResource(ModelResource):
    cursos = fields.ForeignKey('appssgr.api.CursoResource', 'curso',full=True)
    class Meta:
        queryset = Aluno.objects.all()
        resource_name = 'aluno'

class AlunoDisciplinaResource(ModelResource):
    aluno = fields.ForeignKey('appssgr.api.AlunoResource','aluno',full=True)
    disciplina = fields.ForeignKey('appssgr.api.DisciplinaResource', 'disciplina',full=True)
    class Meta:
        queryset = AlunoDisciplina.objects.all()
        always_return_data = True
        resource_name = 'alunodisciplina'

class TipoRequerimentoResource(ModelResource):
    class Meta:
        queryset = TipoRequerimento.objects.all()
        resource_name='tiporequerimento'

class SituacaoResource(ModelResource):
    class Meta:
        queryset = Situacao.objects.all()
        resource_name='situacao'

class RequerimentoResource(ModelResource):
    aluno = fields.ForeignKey('appssgr.api.AlunoResource', 'aluno', full=True)
    tipo = fields.ForeignKey('appssgr.api.TipoRequerimentoResource','tipo_requerimento',full=True)
    disciplina = fields.ForeignKey('appssgr.api.DisciplinaResource', 'disciplina', full=True)
    professor = fields.ForeignKey('appssgr.api.ProfessorResource', 'professor_atividade', full=True)
    situacao = fields.ForeignKey('appssgr.api.SituacaoResource', 'situacao', full=True)
    class Meta:
        queryset = Requerimento.objects.all()
        resource_name = 'requerimento'













