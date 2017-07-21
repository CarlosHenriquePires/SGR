from appsgr.models import *

# Criando as pessoas
pes1=Pessoa(idpessoa=1,nome='Givanaldo', sobrenome="Rocha", cpf='33344455561',
            email='givanaldo@gmail.com',data_nascimento="1973-01-12", telefone='8499253259')
pes1.save()

pes2=Pessoa(idpessoa=2,nome='Bruno', sobrenome="Gomes", cpf='33344455562',
            email='brunao@gmail.com',data_nascimento="1973-01-12", telefone='8499253259')
pes2.save()

pes3=Pessoa(idpessoa=3,nome='Demostenes', sobrenome="Sena", cpf='33344455563',
            email='demostenes@gmail.com',data_nascimento="1973-01-12", telefone='8499253259')
pes3.save()

pes4=Pessoa(idpessoa=4,nome='Marcelo', sobrenome="Varela", cpf='33344455564',
            email='marcelovarela@gmail.com',data_nascimento="1973-01-12", telefone='8499253259')
pes4.save()

pes5=Pessoa(idpessoa=5,nome='Fábio', sobrenome="Procópio", cpf='33344455565',
            email='procopio@gmail.com',data_nascimento="1973-01-12", telefone='8499253259')
pes5.save()

pes6=Pessoa(idpessoa=6,nome='Eduardo', sobrenome="Chavez", cpf='33344455566',
            email='eduardo@gmail.com',data_nascimento="1973-01-12",telefone='8499253259')
pes6.save()

pes7=Pessoa(idpessoa=7,nome='Carlos Henrique', sobrenome='Pires dos Santos', cpf='33344455567',
              email='carlos@gmail.com',data_nascimento="1973-01-12", telefone='8499253259')
pes7.save()

pes8=Pessoa(idpessoa=8,nome='Matheus Barbosa', sobrenome='de Farias', cpf='33344455568',
              email='matheuzin@gmail.com',data_nascimento="1973-01-12", telefone='8499253259')
pes8.save()

pes9=Pessoa(idpessoa=9,nome='Juliana', sobrenome="Soares", cpf='33344455569',
            email='juliana@gmail.com',data_nascimento="1973-01-12", telefone='8499253259')
pes9.save()

pes10=Pessoa(idpessoa=10,nome='Luan', sobrenome="Medeiros", cpf='33344455570',
            email='luanmedeiros@gmail.com',data_nascimento="1973-01-12", telefone='8499253259')
pes10.save()

# Criação dos Grupos para as permissões
professores=Group(name="Professores")
professores.save()
coordenadores=Group(name="Coordenadores")
coordenadores.save()
alunos=Group(name="Alunos")
alunos.save()
tecadm=Group(name="Técnico Administrativo")
tecadm.save()


#Professores
prof1=Professor(pessoa=pes1,username='20122148000001')
prof1.set_password('123456')
prof1.save()
professores.user_set.add(prof1)
coordenadores.user_set.add(prof1)


prof2=Professor(pessoa=pes2,username='20122148000002')
prof2.set_password('123456')
prof2.save()
professores.user_set.add(prof2)
coordenadores.user_set.add(prof2)

prof3=Professor(pessoa=pes3,username='20122148000003')
prof3.set_password('123456')
prof3.save()
professores.user_set.add(prof3)

prof4=Professor(pessoa=pes4,username='20122148000004')
prof4.set_password('123456')
prof4.save()
professores.user_set.add(prof4)

prof5=Professor(pessoa=pes5,username='20122148000005')
prof5.set_password('123456')
prof5.save()
professores.user_set.add(prof5)

# Coordenadores

#Tec Admin
tecadm1=Tecnico_Administrativo(pessoa=pes6,username='20122148000006')
tecadm1.set_password('123456')
tecadm1.save()
tecadm.user_set.add(tecadm1)


# Criando as Disciplinas
web1 = Disciplina(codigo="prowb1", nome="Programação Web I", carga_horaria=60, periodo=2)
web1.save()
estd = Disciplina(codigo="estd", nome="Estrutura de Dados", carga_horaria=60, periodo=2)
estd.save()
algo = Disciplina(codigo="algo", nome="Algoritmo", carga_horaria=60, periodo=1)
algo.save()
bd1 = Disciplina(codigo="bd1", nome="Banco de Dados I", carga_horaria=60, periodo=3)
bd1.save()

# Criando o Curso
tsi = Curso(codigo="tsi14", nome="Tecnólogo Sistemas para Internet")
tsi.save()

# Criando os Alunos

alu1=Aluno(pessoa=pes7,curso=tsi,username='20122148000007')
alu1.set_password('123456')
alu1.save()
alunos.user_set.add(alu1)

alu2=Aluno(pessoa=pes8,curso=tsi,username='20122148000008')
alu2.set_password('123456')
alu2.save()
alunos.user_set.add(alu2)

alu3=Aluno(pessoa=pes9,curso=tsi,username='20122148000009')
alu3.set_password('123456')
alu3.save()
alunos.user_set.add(alu3)

alu4=Aluno(pessoa=pes10,curso=tsi,username='20122148000010')
alu4.set_password('123456')
alu4.save()
alunos.user_set.add(alu4)

# Alunos se matriculando nas Disciplinas
aludisc = AlunoDisciplina(aluno=alu1,disciplina=web1,matriculado=True)
aludisc.save()

aludisc2 = AlunoDisciplina(aluno=alu1,disciplina=bd1,matriculado=True)
aludisc2.save()

aludisc3 = AlunoDisciplina(aluno=alu2,disciplina=estd,matriculado=True)
aludisc3.save()

aludisc4 = AlunoDisciplina(aluno=alu2,disciplina=algo,matriculado=True)
aludisc4.save()

aludisc5 = AlunoDisciplina(aluno=alu3,disciplina=bd1,matriculado=True)
aludisc5.save()

aludisc6 = AlunoDisciplina(aluno=alu3,disciplina=algo,matriculado=True)
aludisc6.save()

aludisc7 = AlunoDisciplina(aluno=alu4,disciplina=web1,matriculado=True)
aludisc7.save()

aludisc8 = AlunoDisciplina(aluno=alu4,disciplina=estd,matriculado=True)
aludisc8.save()

# Tipo Requerimento
tipo1 = TipoRequerimento(nome="Reposição de Atividades")
tipo1.save()

# Documento
doc1 = Documento(nome="Atestado Médico")
doc1.save()
doc2 = Documento(nome="Declaração")
doc2.save()

# Situação
sit1 = Situacao(tipo="Em Avaliação")
sit1.save()
sit2 = Situacao(tipo="Requerimento Deferido")
sit2.save()
sit3 = Situacao(tipo="Requerimento Indeferido")
sit3.save()
