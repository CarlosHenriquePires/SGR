from django.db import models
from django.contrib.auth.models import User, Group


# Modelo Pessoa
class Pessoa(User):
    data_nascimento = models.DateField("Data de Nascimento", null=True, blank=True)
    cpf = models.CharField("CPF", max_length=14, unique=True, null=False, blank=False)
    telefone = models.CharField("Telefone",max_length=11, blank=True, null=True)

    def __str__(self):
        return self.pessoa.first_name


# Modelo Professor
class Professor(models.Model):
    pessoa = models.OneToOneField(Pessoa, on_delete=models.PROTECT, verbose_name="Pessoa", null=False, primary_key=True)

    def __str__(self):
        return self.pessoa.first_name

# Modelo Tecnico Administrativo
class Tecnico_Administrativo(models.Model):
    pessoa = models.OneToOneField(Pessoa, on_delete=models.PROTECT, verbose_name="Pessoa", null=False,primary_key=True)

    def __str__(self):
        return self.pessoa.first_name

# Modelo Curso
class Curso(models.Model):
    codigo = models.CharField("Codigo Curso", max_length=6, primary_key=True)
    nome = models.CharField("Nome", max_length=50, null=False)

    def __str__(self):
        return self.nome

# Modelo Aluno
class Aluno(Pessoa):
    #pessoa = models.OneToOneField(Pessoa, on_delete=models.PROTECT, verbose_name="Pessoa", null=False, primary_key=True)
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT, verbose_name="Curso", null=False, blank=False)

    def __str__(self):
        return self.pessoa.first_name

# Modelo Disciplina
class Disciplina(models.Model):
    codigo = models.CharField("Codigo Disciplina", max_length=6, primary_key=True)
    nome = models.CharField("Nome", max_length=50, null=False)
    carga_horaria = models.IntegerField("Carga Horária", null=False)
    professor = models.ManyToManyField(Professor)
    periodo = models.IntegerField("Período", null=False, blank=False)
    aluno = models.ManyToManyField(Aluno,through="AlunoDisciplina")
    curso = models.ManyToManyField(Curso)

    def __str__(self):
        return self.nome

# Modelo AlunoDisciplina
class AlunoDisciplina(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.PROTECT)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.PROTECT)
    matriculado = models.BooleanField("matriculado", blank=False, null=False)

# Modelo TipoRequerimento
class TipoRequerimento(models.Model):
    nome = models.CharField("Nome Documento", max_length=150, null=False)

    def __str__(self):
        return self.nome

    class Meta:
        permissions = (
        ("view_tipo_requerimento", "Can see tipo requerimento"),("detail_tipo_requerimento", "Can see detail of the tipo requerimento"))

# Modelo Documento
class Documento(models.Model):
    nome = models.CharField("Nome Documento", max_length=150, null=False)

    def __str__(self):
        return self.nome

class Situacao(models.Model):
    tipo = models.CharField("Tipo da Situação", max_length=150, null=False)

    def __str__(self):
        return self.tipo

# Função do caminho do diretório
def aluno_directory_path(instance, filename):
    return 'func_{0}/{1}'.format(instance.aluno.username, filename)

class Requerimento(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.PROTECT, related_name="Aluno", null=False)
    data_solicitacao_requerimento = models.DateTimeField("Data da solicitação", null=True, blank=True, auto_now_add=True, editable=False)
    tipo_requerimento = models.ForeignKey(TipoRequerimento, on_delete=models.PROTECT, verbose_name="Tipo de Requerimento", null=False)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.PROTECT, related_name="Disciplina", null=True, blank=True)
    observacoes = models.TextField("Observações", blank=True, null=True)
    justificativa = models.TextField("Justificativa", blank=True, null=True)
    data_atividade = models.DateField("Data da atividade", null=True, blank=True)
    tipo_atividade = models.CharField("Tipo de atividade", max_length=50, null=True, blank=True)
    professor_atividade = models.ForeignKey(Professor, on_delete=models.PROTECT, related_name="Professor_Atividade", null=True, blank=True)
    documentos_apresentados = models.ManyToManyField(Documento, blank=True)
    documentos_files = models.FileField(upload_to=aluno_directory_path,default=None, null=True)
    encaminhado_para = models.ForeignKey(Pessoa, on_delete=models.PROTECT, related_name="Avaliador", null=True, blank=True)
    situacao = models.ForeignKey(Situacao, max_length=50, blank=True, null=True,default=1)

    class Meta:
        permissions = (
        ("view_requerimento", "Can see requerimento"),("detail_requerimento", "Can see detail of the requerimento"))

    def file_link(self):
        if self.documentos_files:
            return "<a href='%s'>Download</a>" % (self.documentos_files.url,)
        else:
            return "Nenhum anexo"

    file_link.allow_tags = True