from appsgr.models import *

professores=Group(name="Professores")
professores.save()
coordenadores=Group(name="Coordenadores")
coordenadores.save()
alunos=Group(name="Alunos")
alunos.save()
tecadm=Group(name="Técnico Administrativo")
tecadm.save()

# Criando as pessoas
pes1=Pessoa(is_staff=True,first_name='Givanaldo', last_name="Rocha", cpf='33344455560',email='givanaldo@gmail.com',
            data_nascimento="1973-05-30", telefone='8499253259' ,username='20122148000001')
pes1.set_password('123456')
pes1.save()
professores.user_set.add(pes1)

pes2=Pessoa(is_staff=True,first_name='João Maria', last_name='Joaozin', cpf='33344455565',email='joaozin@gmail.com',
            data_nascimento="1977-05-30", telefone='84998217952' ,username='20122148000007')
pes2.set_password('123456')
pes2.save()
professores.user_set.add(pes2)

pes3=Pessoa(is_staff=True,first_name='Demostenes', last_name='Sena', cpf='33344455566',email='demostenes@gmail.com',
            data_nascimento="1970-05-15", telefone='84998217913' ,username='20122148000008')
pes3.set_password('123456')
pes3.save()
professores.user_set.add(pes3)

pes5=Pessoa(is_staff=True,first_name='Bruno', last_name='Gomes', cpf='33344455567',email='bruno@gmail.com',
            data_nascimento="1970-05-15", telefone='84998212913' ,username='20122148000009')
pes5.set_password('123456')
pes5.save()
professores.user_set.add(pes5)
coordenadores.user_set.add(pes5)

pes4=Tecnico_Administrativo(first_name='Eduardo', last_name="Chavez", cpf='55566633301',email='eduardo@gmail.com',data_nascimento="1989-05-15",username='20122148000004',  telefone='84955196660')
pes4.set_password('123456')
pes4.save()
tecadm.user_set.add(pes4)

# Criando as Disciplinas
web1 = Disciplina(codigo="prowb1", nome="Programação Web I", carga_horaria=60, periodo=2)
web1.save()
estd = Disciplina(codigo="estd", nome="Estrutura de Dados", carga_horaria=60, periodo=2)
estd.save()
algo = Disciplina(codigo="algo", nome="Algoritmo", carga_horaria=60, periodo=1)
algo.save()

# Criando o Curso
tsi = Curso(codigo="tsi14", nome="Tecnólogo Sistemas para Internet")
tsi.save()

# Criando os Alunos
alu1=Aluno(is_staff=True,first_name='Carlos Henrique', last_name='Pires dos Santos', cpf='33344455561',email='carlos@gmail.com',
            data_nascimento="1999-05-30", telefone='84998217953' ,username='20122148000002',curso=tsi)
alu1.set_password('123456')
alu1.save()
alunos.user_set.add(alu1)

alu2=Aluno(is_staff=True,first_name='Juliana', last_name='dos Anjos', cpf='33344455562',email='juh@gmail.com',
            data_nascimento="1999-05-15", telefone='84998217913' ,username='20122148000003',curso=tsi)
alu2.set_password('123456')
alu2.save()
alunos.user_set.add(alu2)

alu3=Aluno(is_staff=True,first_name='Matheus Barbosa', last_name='Farias', cpf='33344455563',email='matheuzin@gmail.com',
            data_nascimento="1999-08-20", telefone='84998217953' ,username='20122148000005',curso=tsi)
alu3.set_password('123456')
alu3.save()
alunos.user_set.add(alu3)

alu4=Aluno(is_staff=True,first_name='Luan Medeiro', last_name='Jr', cpf='33344455564',email='luandalua@gmail.com',
            data_nascimento="1999-02-11", telefone='84998217913' ,username='20122148000006',curso=tsi)
alu4.set_password('123456')
alu4.save()
alunos.user_set.add(alu4)

# Alunos se matriculando nas Disciplinas
aludisc = AlunoDisciplina(aluno=alu1,disciplina=web1,matriculado=True)
aludisc.save()

# Tipo Requerimento
tipo1 = TipoRequerimento(nome="Reposição de Atividades")
tipo1.save()

# Documento
doc1 = Documento(nome="Atestado Médico")
doc1.save()

# Situação
sit1 = Situacao(tipo="Em Avaliação")
sit1.save()
sit2 = Situacao(tipo="Requerimento Deferido")
sit2.save()
sit3 = Situacao(tipo="Requerimento Indeferido")
sit3.save()
