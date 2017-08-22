from django.contrib.auth.decorators import login_required,permission_required
from django.shortcuts import render,redirect
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.template import Context
from appsgr.forms import *
from django.forms import modelform_factory
from django.http import HttpResponse
from django.core.mail import send_mail

@login_required(login_url='login')
@permission_required('appsgr.detail_requerimento',login_url='erro_permissao')
def req_detail_pdf(request, pk):
    pessoa_logada = Aluno.objects.get(username=request.user.username)
    usuarios = []
    request.session[0]=pk
    try:
        aluno = Aluno.objects.get(username=pessoa_logada.username)
    except Aluno.DoesNotExist:
        aluno = None
    requerimento=Requerimento.objects.get(id=pk)
    form=RequerimentoForm(request.POST,instance=requerimento)
    dados = {'form':form,'usuarios':usuarios,'requerimento':requerimento}

    # convertendo para PDF
    template = get_template('req/pdf.html')
    html = template.render(Context(dados))
    file = open('comprovante.pdf', "w+b")
    pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file,
            encoding='utf-8')
    file.seek(0)
    pdf = file.read()
    file.close()
    return HttpResponse(pdf, 'application/pdf')

@login_required(login_url='login')
def home(request):
   return render(request,'base.html')

@login_required(login_url='login')
def curso(request):
    return render(request,'curso.html')

@login_required(login_url='login')
def erro_permissao(request):
    return render(request,'req/erro_permissao.html')

@login_required(login_url='login')
def ok(request):
    return render(request, 'req/ok.html')

@login_required(login_url='login')
@permission_required('appsgr.add_requerimento',login_url='erro_permissao')
def req_new(request):
    if (request.method=="GET"):
        id_tipo_requerimento = request.GET.get("id_tipo_requerimento")
        request.session[0]=id_tipo_requerimento
    else:
        id_tipo_requerimento=request.session['0']

    if(id_tipo_requerimento=="1"):
        RequerimentoFormNovo=modelform_factory(Requerimento,fields=('professor_atividade','tipo_atividade','disciplina','data_atividade','justificativa','documentos_apresentados','documentos_files',))

    if (request.method=="POST"):
        form=RequerimentoFormNovo(request.POST,request.FILES)
        if (form.is_valid()):
            requerimento=form.save(commit=False)
            requerimento.tipo_requerimento=TipoRequerimento.objects.get(id=id_tipo_requerimento)
            requerimento.aluno = Aluno.objects.get(username=request.user.username)
            requerimento.save()
            email = 'Atenção! Um novo requerimento foi solicitado pelo aluno {} {}, de matrícula {}, ' \
                    'do curso {} para a disciplina {}. Favor checar o sistema. '.format\
                (requerimento.aluno.pessoa.nome,requerimento.aluno.pessoa.sobrenome,
                 requerimento.aluno.username,requerimento.aluno.curso.nome,requerimento.disciplina)

            send_mail('Novo Requerimento Solicitado!', email, 'notificacao.sgr@gmail.com',
                      ['carluxhenrique@gmail.com'], fail_silently=False)
            return render(request, 'req/ok.html')
    else:
        form=RequerimentoFormNovo()
    dados={'form':form}
    return render(request, 'req/req_form.html', dados)

@login_required(login_url='login')
@permission_required('appsgr.add_requerimento',login_url='erro_permissao')
def req_list(request):
    pessoa_logada = User.objects.get(username=request.user.username)
    tipo_requerimento=TipoRequerimento.objects.all().order_by('nome')

    #Instanciando objetos
    try:
        aluno = Aluno.objects.get(username=pessoa_logada.username)
    except Aluno.DoesNotExist:
        aluno = None

    #ALUNO
    if(aluno != None):
        dados={"tipo_requerimento":tipo_requerimento}
        return render(request, 'req/req_criar.html', dados)


@login_required(login_url='login')
@permission_required('appsgr.view_requerimento',login_url='erro_permissao')
def req_list_avaliacao(request):
    criterio = request.GET.get('criterio')
    criterio_prof = request.GET.get('professores')
    criterio_disciplina = request.GET.get('disciplinas')
    pessoa_logada = User.objects.get(username=request.user.username)
    tipo_requerimento = TipoRequerimento.objects.all().order_by('nome')
    professores = Professor.objects.all().order_by('pessoa__nome')
    disciplinas = Disciplina.objects.all().order_by('nome')
    requerimentos_professor = []

    # Instanciando objetos
    try:
        aluno = Aluno.objects.get(username=pessoa_logada.username)
    except Aluno.DoesNotExist:
        aluno = None
    try:
        coordenador = Coordenador.objects.get(username=pessoa_logada.username)
    except Coordenador.DoesNotExist:
        coordenador = None

    try:
        professor = Professor.objects.get(username=pessoa_logada.username)
    except Professor.DoesNotExist:
        professor = None

    try:
        tecnico = Tecnico_Administrativo.objects.get(username=pessoa_logada.username)
    except Tecnico_Administrativo.DoesNotExist:
        tecnico = None

    # ALUNO
    if (aluno != None):
            if (criterio_prof):
                requerimento = Requerimento.objects.filter(situacao=1, aluno=aluno,
                                                           professor_atividade__pessoa__nome__contains=criterio_prof,
                                                           ).order_by('data_solicitacao_requerimento')
            if (criterio_disciplina):
                requerimento = Requerimento.objects.filter(aluno=aluno, situacao=1,
                                                           disciplina__disciplina__nome__contains=criterio_disciplina).order_by(
                    'data_solicitacao_requerimento')

            if (criterio_prof or criterio_disciplina):
                requerimento = Requerimento.objects.filter(aluno=aluno, situacao=1,
                                                           professor_atividade__pessoa__nome__contains=criterio_prof
                                                           ,
                                                           disciplina__disciplina__nome__contains=criterio_disciplina).order_by \
                    ('data_solicitacao_requerimento')


            else:
                requerimento = Requerimento.objects.all().filter(aluno=aluno, situacao=1).order_by(
                    'data_solicitacao_requerimento')
                criterio = ""
            # Cria o mecanimos de paginação
            paginator = Paginator(requerimento, 10)
            page = request.GET.get('page')
            try:
                requerimento = paginator.page(page)
            except PageNotAnInteger:
                requerimento = paginator.page(1)
            except EmptyPage:
                requerimento = paginator.page(paginator.num_pages)
            dados = {'requerimento': requerimento, 'criterio': criterio, 'paginator': paginator,
                     'page_obj': requerimento,
                     "tipo_requerimento": tipo_requerimento, "professores": professores, "disciplinas": disciplinas,
                     'requerimentos_professor': requerimentos_professor}
            return render(request, 'req/req_list_aluno.html', dados)

    # COORDENADOR
    elif (coordenador != None):
        if (criterio):
            requerimento = Requerimento.objects.filter(situacao=1,encaminhado_para=pessoa_logada,
                                                       aluno__pessoa__nome__contains=criterio).order_by(
                'tipo_requerimento', 'data_solicitacao_requerimento')

        if (criterio_prof):
            requerimento = Requerimento.objects.filter(situacao=1,encaminhado_para=pessoa_logada,
                                                       professor_atividade__pessoa__nome__contains=criterio_prof)
                           #| Requerimento.objects.all().filter(professor_atividade__pessoa__nome__contains=professor.pessoa.nome,situacao=1).order_by\
                            #   ('data_solicitacao_requerimento','aluno__pessoa__nome')
        if (criterio_disciplina):
            requerimento = Requerimento.objects.filter(encaminhado_para=pessoa_logada,situacao=1,
                                                       disciplina__disciplina__nome__contains=criterio_disciplina).order_by(
                'data_solicitacao_requerimento','aluno__pessoa__nome')

        if (criterio_prof or criterio or criterio_disciplina ):
            requerimento = Requerimento.objects.filter(encaminhado_para=pessoa_logada,situacao=1, professor_atividade__pessoa__nome__contains=criterio_prof
            ,aluno__pessoa__nome__contains=criterio,disciplina__disciplina__nome__contains=criterio_disciplina)
                           #| Requerimento.objects.all().filter(professor_atividade__pessoa__nome__contains=professor.pessoa.nome,situacao=1).order_by\
                            #   ('data_solicitacao_requerimento','aluno__pessoa__nome')

        else:
            requerimento = Requerimento.objects.all().filter(encaminhado_para=pessoa_logada,situacao=1) | Requerimento.objects.all().filter\
                (encaminhado_para=pessoa_logada,professor_atividade=pessoa_logada,situacao=1).order_by(
                'data_solicitacao_requerimento','aluno__pessoa__nome')
            criterio = ""
        # Cria o mecanimos de paginação
        paginator = Paginator(requerimento, 10)
        page = request.GET.get('page')
        try:
            requerimento = paginator.page(page)
        except PageNotAnInteger:
            requerimento = paginator.page(1)
        except EmptyPage:
            requerimento = paginator.page(paginator.num_pages)
        dados = {'requerimento': requerimento,'criterio': criterio, 'paginator': paginator, 'page_obj': requerimento,
                 "tipo_requerimento": tipo_requerimento, "professores": professores,"disciplinas": disciplinas,'requerimentos_professor': requerimentos_professor}
        return render(request, 'req/req_list_coor.html', dados)

    # PROFESSOR
    elif (professor != None):
        if (criterio):
            requerimento = Requerimento.objects.filter(professor_atividade=pessoa_logada,situacao=1).order_by(
                'data_solicitacao_requerimento','aluno__pessoa__nome')
        if (criterio_disciplina):
            requerimento = Requerimento.objects.filter(professor_atividade=pessoa_logada, situacao=1,
                                                       disciplina__disciplina__nome__contains=criterio_disciplina).order_by(
                'data_solicitacao_requerimento','aluno__pessoa__nome')

        if (criterio or criterio_disciplina):
            requerimento = Requerimento.objects.filter(professor_atividade=pessoa_logada,situacao=1,
            aluno__pessoa__nome__contains=criterio,disciplina__disciplina__nome__contains=criterio_disciplina).order_by\
                ('data_solicitacao_requerimento','aluno__pessoa__nome')

        else:
            requerimento = Requerimento.objects.all().filter(professor_atividade=pessoa_logada,situacao=1).order_by(
                'data_solicitacao_requerimento','aluno__pessoa__nome')
            criterio = ""
        # Cria o mecanimos de paginação
        paginator = Paginator(requerimento, 10)
        page = request.GET.get('page')
        try:
            requerimento = paginator.page(page)
        except PageNotAnInteger:
            requerimento = paginator.page(1)
        except EmptyPage:
            requerimento = paginator.page(paginator.num_pages)
        dados = {'requerimento': requerimento, 'criterio': criterio, 'paginator': paginator, 'page_obj': requerimento,
                 "tipo_requerimento": tipo_requerimento, "professores": professores,"disciplinas": disciplinas,'requerimentos_professor': requerimentos_professor}
        return render(request, 'req/req_list_prof.html', dados)

    # TECNICO ADMINISTRATIVO
    elif (tecnico != None):
        if (criterio):
            requerimento = Requerimento.objects.filter(encaminhado_para=None,situacao=1,
                                                       aluno__pessoa__nome__contains=criterio).order_by(
                'tipo_requerimento', 'data_solicitacao_requerimento')

        if (criterio_prof):
            requerimento = Requerimento.objects.filter(encaminhado_para=None,situacao=1, professor_atividade__pessoa__nome__contains=criterio_prof,
                                                       ).order_by('data_solicitacao_requerimento','aluno__pessoa__nome')
        if (criterio_disciplina):
            requerimento = Requerimento.objects.filter(encaminhado_para=None,situacao=1,
                                                       disciplina__disciplina__nome__contains=criterio_disciplina).order_by(
                'data_solicitacao_requerimento','aluno__pessoa__nome')

        if (criterio_prof or criterio or criterio_disciplina ):
            requerimento = Requerimento.objects.filter(encaminhado_para=None,situacao=1, professor_atividade__pessoa__nome__contains=criterio_prof
            ,aluno__pessoa__nome__contains=criterio,disciplina__disciplina__nome__contains=criterio_disciplina).order_by\
                ('data_solicitacao_requerimento','aluno__pessoa__nome')


        else:
            requerimento = Requerimento.objects.all().filter(encaminhado_para=None,situacao=1).order_by(
                'data_solicitacao_requerimento','aluno__pessoa__nome')
            criterio = ""
        # Cria o mecanimos de paginação
        paginator = Paginator(requerimento, 10)
        page = request.GET.get('page')
        try:
            requerimento = paginator.page(page)
        except PageNotAnInteger:
            requerimento = paginator.page(1)
        except EmptyPage:
            requerimento = paginator.page(paginator.num_pages)
        dados = {'requerimento': requerimento, 'criterio': criterio, 'paginator': paginator, 'page_obj': requerimento,
                 "tipo_requerimento": tipo_requerimento, "professores": professores,"disciplinas": disciplinas,'requerimentos_professor': requerimentos_professor}
        return render(request, 'req/req_list_tecnico.html', dados)

@login_required(login_url='login')
@permission_required('appsgr.detail_requerimento',login_url='erro_permissao')
def req_detail(request, pk):
    pessoa_logada = User.objects.get(username=request.user.username)
    usuarios = []
    request.session[0]=pk
    try:
        aluno = Aluno.objects.get(username=pessoa_logada.username)
    except Aluno.DoesNotExist:
        aluno = None
    try:
        professor = Professor.objects.get(username=pessoa_logada.username)
    except Professor.DoesNotExist:
        professor = None
    try:
        coordenador = Coordenador.objects.get(username=pessoa_logada.username)
    except Coordenador.DoesNotExist:
        coordenador = None
    try:
        tecnico = Tecnico_Administrativo.objects.get(username=pessoa_logada.username)
    except Tecnico_Administrativo.DoesNotExist:
        tecnico = None

    requerimento=Requerimento.objects.get(id=pk)
    form=RequerimentoForm(request.POST,instance=requerimento)
    dados = {'form':form,'usuarios':usuarios,'requerimento':requerimento}
    return render(request, 'req/req_detail.html', dados)

@login_required(login_url='login')
@permission_required('appsgr.change_requerimento',login_url='erro_permissao')
def req_update(request,pk):
    requerimento=Requerimento.objects.get(id=pk)
    if (request.method=="POST"):
        form=RequerimentoFormUpdate(request.POST,request.FILES,instance=requerimento)
        if (form.is_valid()):
            form.save()
            situacao = "Em Avaliação"
            if (requerimento.situacao.tipo != situacao):
                email = 'Atenção! Caro aluno, {} {} de matrícula {}, ' \
                        'do curso {}, a situação do requerimento solicitado para a disciplina {}, foi alterado para {}.' \
                        ' Favor checar o sistema. '.format(
                    requerimento.aluno.pessoa.nome, requerimento.aluno.pessoa.sobrenome, requerimento.aluno.username,
                    requerimento.aluno.curso.nome, requerimento.disciplina, requerimento.situacao)

                send_mail('Situação do Requerimento foi Atualizada!', email, 'notificacao.sgr@gmail.com',
                          ['carluxhenrique@gmail.com'], fail_silently=False)
            if (requerimento.situacao.tipo == situacao and requerimento.encaminhado_para != None):
                email = 'Atenção! Caro aluno, {} {} de matrícula {}, ' \
                        'do curso {}, o requerimento solicitado para a disciplina {}, foi encaminhado para o Coordenador {} {}. ' \
                        'Favor checar o sistema para mais informações.'.format(
                    requerimento.aluno.pessoa.nome, requerimento.aluno.pessoa.sobrenome, requerimento.aluno.username,
                    requerimento.aluno.curso.nome, requerimento.disciplina, requerimento.encaminhado_para.first_name,requerimento.encaminhado_para.last_name)
                email2 = 'Atenção! O Técnico Administrativo acabou de lhe encaminhar o requerimento solicitado pelo aluno {} {}, de matrícula {}, ' \
                    'do curso {} para a disciplina {}. Favor checar o sistema. '.format\
                (requerimento.aluno.pessoa.nome,requerimento.aluno.pessoa.sobrenome,
                 requerimento.aluno.username,requerimento.aluno.curso.nome,requerimento.disciplina)
                send_mail('Requerimento Encaminhado ao Coordenador!', email, 'notificacao.sgr@gmail.com',
                          ['carluxhenrique@gmail.com'], fail_silently=False)
                send_mail('Requerimento Encaminhado ao Coordenador!', email2, 'notificacao.sgr@gmail.com',
                          ['carluxhenrique@gmail.com'], fail_silently=False)

            return render(request, 'req/ok.html')

    else:
        form=RequerimentoFormUpdate(instance=requerimento)
        dados={'form':form}
        return render(request, 'req/req_form_update.html', dados)

##############

@login_required(login_url='login')
@permission_required('appsgr.view_tipo_requerimento',login_url='erro_permissao')
def req_list_deferidos(request):
    criterio = request.GET.get('criterio')
    criterio_prof = request.GET.get('professores')
    criterio_disciplina = request.GET.get('disciplinas')
    pessoa_logada = User.objects.get(username=request.user.username)
    tipo_requerimento = TipoRequerimento.objects.all().order_by('nome')
    professores = Professor.objects.all().order_by('pessoa__nome')
    disciplinas = Disciplina.objects.all().order_by('nome')
    requerimentos_professor = []

    #Instanciando objetos
    try:
        aluno = Aluno.objects.get(username=pessoa_logada.username)
    except Aluno.DoesNotExist:
        aluno = None
    try:
        coordenador = Coordenador.objects.get(username=pessoa_logada.username)
    except Coordenador.DoesNotExist:
        coordenador = None
    try:
        professor = Professor.objects.get(username=pessoa_logada.username)
    except Professor.DoesNotExist:
        professor = None
    try:
        tecnico = Tecnico_Administrativo.objects.get(username=pessoa_logada.username)
    except Tecnico_Administrativo.DoesNotExist:
        tecnico = None

        # ALUNO
    if (aluno != None):
            if (criterio_prof):
                requerimento = Requerimento.objects.filter(situacao=2, aluno=aluno,
                                                           professor_atividade__pessoa__nome__contains=criterio_prof,
                                                           ).order_by('data_solicitacao_requerimento')
            if (criterio_disciplina):
                requerimento = Requerimento.objects.filter(aluno=aluno, situacao=2,
                                                           disciplina__disciplina__nome__contains=criterio_disciplina).order_by(
                    'data_solicitacao_requerimento')

            if (criterio_prof or criterio_disciplina):
                requerimento = Requerimento.objects.filter(aluno=aluno, situacao=2,
                                                           professor_atividade__pessoa__nome__contains=criterio_prof
                                                           ,
                                                           disciplina__disciplina__nome__contains=criterio_disciplina).order_by \
                    ('data_solicitacao_requerimento')


            else:
                requerimento = Requerimento.objects.all().filter(aluno=aluno, situacao=2).order_by(
                    'data_solicitacao_requerimento')
                criterio = ""
            # Cria o mecanimos de paginação
            paginator = Paginator(requerimento, 10)
            page = request.GET.get('page')
            try:
                requerimento = paginator.page(page)
            except PageNotAnInteger:
                requerimento = paginator.page(1)
            except EmptyPage:
                requerimento = paginator.page(paginator.num_pages)
            dados = {'requerimento': requerimento, 'criterio': criterio, 'paginator': paginator,
                     'page_obj': requerimento,
                     "tipo_requerimento": tipo_requerimento, "professores": professores, "disciplinas": disciplinas,
                     'requerimentos_professor': requerimentos_professor}
            return render(request, 'req/req_list_deferidos.html', dados)

    # COORDENADOR
    elif (coordenador != None):
        if (criterio):
            requerimento = Requerimento.objects.filter(situacao=2, encaminhado_para=pessoa_logada,
                                                           aluno__pessoa__nome__contains=criterio).order_by(
                    'tipo_requerimento', 'data_solicitacao_requerimento')

        if (criterio_prof):
            requerimento = Requerimento.objects.filter(situacao=2, encaminhado_para=pessoa_logada,
                                                           professor_atividade__pessoa__nome__contains=criterio_prof)
                           #| Requerimento.objects.all().filter(
                    #professor_atividade__pessoa__nome__contains=professor.pessoa.nome, situacao=2).order_by \
                     #              ('data_solicitacao_requerimento', 'aluno__pessoa__nome')
        if (criterio_disciplina):
            requerimento = Requerimento.objects.filter(encaminhado_para=pessoa_logada, situacao=2,
                                                           disciplina__disciplina__nome__contains=criterio_disciplina).order_by(
                    'data_solicitacao_requerimento', 'aluno__pessoa__nome')

        if (criterio_prof or criterio or criterio_disciplina):
            requerimento = Requerimento.objects.filter(encaminhado_para=pessoa_logada, situacao=2,
                                                           professor_atividade__pessoa__nome__contains=criterio_prof
                                                           , aluno__pessoa__nome__contains=criterio,
                                                           disciplina__disciplina__nome__contains=criterio_disciplina)\
                           #| Requerimento.objects.all().filter(
                    #professor_atividade__pessoa__nome__contains=professor.pessoa.nome, situacao=2).order_by \
                     #              ('data_solicitacao_requerimento', 'aluno__pessoa__nome')

        else:
            requerimento = Requerimento.objects.all().filter(encaminhado_para=pessoa_logada,
                                                                 situacao=2) | Requerimento.objects.all().filter \
                                   (professor_atividade=pessoa_logada, situacao=2).order_by(
                    'data_solicitacao_requerimento', 'aluno__pessoa__nome')
            criterio = ""
        # Cria o mecanimos de paginação
        paginator = Paginator(requerimento, 10)
        page = request.GET.get('page')
        try:
            requerimento = paginator.page(page)
        except PageNotAnInteger:
            requerimento = paginator.page(1)
        except EmptyPage:
            requerimento = paginator.page(paginator.num_pages)
        dados = {'requerimento': requerimento, 'criterio': criterio, 'paginator': paginator, 'page_obj': requerimento,
                 "tipo_requerimento": tipo_requerimento, "professores": professores, "disciplinas": disciplinas,
                 'requerimentos_professor': requerimentos_professor}
        return render(request, 'req/req_list_deferidos.html', dados)

    # PROFESSOR
    elif(professor != None):
        if (criterio):
            requerimento = Requerimento.objects.filter( situacao=2,professor_atividade=pessoa_logada,
                                                       aluno__pessoa__nome__contains=criterio).order_by(
                'data_solicitacao_requerimento','aluno__pessoa__nome')
        if (criterio_disciplina):
            requerimento = Requerimento.objects.filter(professor_atividade=pessoa_logada, situacao=2,
                                                       disciplina__disciplina__nome__contains=criterio_disciplina).order_by(
                'data_solicitacao_requerimento','aluno__pessoa__nome')

        if (criterio or criterio_disciplina ):
            requerimento = Requerimento.objects.filter(professor_atividade=pessoa_logada,situacao=2,
            aluno__pessoa__nome__contains=criterio,disciplina__disciplina__nome__contains=criterio_disciplina).order_by\
                ('data_solicitacao_requerimento','aluno__pessoa__nome')
        else:
            requerimento = Requerimento.objects.all().filter(professor_atividade=pessoa_logada,situacao=2).order_by(
                'data_solicitacao_requerimento','aluno__pessoa__nome')
            criterio = ""
        # Cria o mecanimos de paginação
        paginator = Paginator(requerimento, 10)
        page = request.GET.get('page')
        try:
            requerimento = paginator.page(page)
        except PageNotAnInteger:
            requerimento = paginator.page(1)
        except EmptyPage:
            requerimento = paginator.page(paginator.num_pages)
        dados = {'requerimento': requerimento, 'criterio': criterio, 'paginator': paginator, 'page_obj': requerimento,
                 "tipo_requerimento": tipo_requerimento, "professores": professores,"disciplinas": disciplinas,'requerimentos_professor': requerimentos_professor}
        return render(request, 'req/req_list_deferidos.html', dados)


@login_required(login_url='login')
@permission_required('appsgr.view_requerimento',login_url='erro_permissao')
def req_list_indeferidos(request):
    criterio = request.GET.get('criterio')
    criterio_prof = request.GET.get('professores')
    criterio_disciplina = request.GET.get('disciplinas')
    pessoa_logada = User.objects.get(username=request.user.username)
    tipo_requerimento = TipoRequerimento.objects.all().order_by('nome')
    professores = Professor.objects.all().order_by('pessoa__nome')
    disciplinas = Disciplina.objects.all().order_by('nome')
    requerimentos_professor = []

    # Instanciando objetos
    try:
        aluno = Aluno.objects.get(username=pessoa_logada.username)
    except Aluno.DoesNotExist:
        aluno = None
    try:
        coordenador = Coordenador.objects.get(username=pessoa_logada.username)
    except Coordenador.DoesNotExist:
        coordenador = None
    try:
        professor = Professor.objects.get(username=pessoa_logada.username)
    except Professor.DoesNotExist:
        professor = None
    try:
        tecnico = Tecnico_Administrativo.objects.get(username=pessoa_logada.username)
    except Tecnico_Administrativo.DoesNotExist:
        tecnico = None

    # ALUNO
    if (aluno != None):
        if (criterio_prof):
            requerimento = Requerimento.objects.filter(situacao=3, aluno=aluno,
                                                       professor_atividade__pessoa__nome__contains=criterio_prof,
                                                       ).order_by('data_solicitacao_requerimento')
        if (criterio_disciplina):
            requerimento = Requerimento.objects.filter(aluno=aluno, situacao=3,
                                                       disciplina__disciplina__nome__contains=criterio_disciplina).order_by(
                'data_solicitacao_requerimento')

        if (criterio_prof or criterio_disciplina):
            requerimento = Requerimento.objects.filter(aluno=aluno, situacao=3,
                                                       professor_atividade__pessoa__nome__contains=criterio_prof
                                                       ,
                                                       disciplina__disciplina__nome__contains=criterio_disciplina).order_by \
                ('data_solicitacao_requerimento')


        else:
            requerimento = Requerimento.objects.all().filter(aluno=aluno, situacao=3).order_by(
                'data_solicitacao_requerimento')
            criterio = ""
        # Cria o mecanimos de paginação
        paginator = Paginator(requerimento, 10)
        page = request.GET.get('page')
        try:
            requerimento = paginator.page(page)
        except PageNotAnInteger:
            requerimento = paginator.page(1)
        except EmptyPage:
            requerimento = paginator.page(paginator.num_pages)
        dados = {'requerimento': requerimento, 'criterio': criterio, 'paginator': paginator,
                 'page_obj': requerimento,
                 "tipo_requerimento": tipo_requerimento, "professores": professores, "disciplinas": disciplinas,
                 'requerimentos_professor': requerimentos_professor}
        return render(request, 'req/req_list_indeferidos.html', dados)

    # COORDENADOR
    elif (coordenador != None):
        if (criterio):
            requerimento = Requerimento.objects.filter(situacao=3, encaminhado_para=pessoa_logada,
                                                       aluno__pessoa__nome__contains=criterio).order_by(
                'tipo_requerimento', 'data_solicitacao_requerimento')

        if (criterio_prof):
            requerimento = Requerimento.objects.filter(situacao=3, encaminhado_para=pessoa_logada,
                                                       professor_atividade__pessoa__nome__contains=criterio_prof)\
                           #| Requerimento.objects.all().filter(
                #professor_atividade__pessoa__nome__contains=professor.pessoa.nome, situacao=3).order_by \
                 #              ('data_solicitacao_requerimento', 'aluno__pessoa__nome')
        if (criterio_disciplina):
            requerimento = Requerimento.objects.filter(encaminhado_para=pessoa_logada, situacao=3,
                                                       disciplina__disciplina__nome__contains=criterio_disciplina).order_by(
                'data_solicitacao_requerimento', 'aluno__pessoa__nome')

        if (criterio_prof or criterio or criterio_disciplina):
            requerimento = Requerimento.objects.filter(encaminhado_para=pessoa_logada, situacao=3,
                                                       professor_atividade__pessoa__nome__contains=criterio_prof
                                                       , aluno__pessoa__nome__contains=criterio,
                                                       disciplina__disciplina__nome__contains=criterio_disciplina) \
                           #| Requerimento.objects.all().filter(
                #professor_atividade__pessoa__nome__contains=professor.pessoa.nome, situacao=3).order_by \
                 #              ('data_solicitacao_requerimento', 'aluno__pessoa__nome')

        else:
            requerimento = Requerimento.objects.all().filter(encaminhado_para=pessoa_logada,
                                                             situacao=3) | Requerimento.objects.all().filter \
                               (professor_atividade=pessoa_logada, situacao=3).order_by(
                'data_solicitacao_requerimento', 'aluno__pessoa__nome')
            criterio = ""
        # Cria o mecanimos de paginação
        paginator = Paginator(requerimento, 10)
        page = request.GET.get('page')
        try:
            requerimento = paginator.page(page)
        except PageNotAnInteger:
            requerimento = paginator.page(1)
        except EmptyPage:
            requerimento = paginator.page(paginator.num_pages)
        dados = {'requerimento': requerimento, 'criterio': criterio, 'paginator': paginator, 'page_obj': requerimento,
                 "tipo_requerimento": tipo_requerimento, "professores": professores, "disciplinas": disciplinas,
                 'requerimentos_professor': requerimentos_professor}
        return render(request, 'req/req_list_indeferidos.html', dados)

    # PROFESSOR
    elif (professor != None):
        if (criterio):
            requerimento = Requerimento.objects.filter(situacao=3, professor_atividade=pessoa_logada,
                                                       aluno__pessoa__nome__contains=criterio).order_by(
                'data_solicitacao_requerimento', 'aluno__pessoa__nome')
        if (criterio_disciplina):
            requerimento = Requerimento.objects.filter(professor_atividade=pessoa_logada, situacao=3,
                                                       disciplina__disciplina__nome__contains=criterio_disciplina).order_by(
                'data_solicitacao_requerimento', 'aluno__pessoa__nome')

        if (criterio or criterio_disciplina):
            requerimento = Requerimento.objects.filter(professor_atividade=pessoa_logada, situacao=3,
                                                       aluno__pessoa__nome__contains=criterio,
                                                       disciplina__disciplina__nome__contains=criterio_disciplina).order_by \
                ('data_solicitacao_requerimento', 'aluno__pessoa__nome')
        else:
            requerimento = Requerimento.objects.all().filter(professor_atividade=pessoa_logada, situacao=3).order_by(
                'data_solicitacao_requerimento', 'aluno__pessoa__nome')
            criterio = ""
        # Cria o mecanimos de paginação
        paginator = Paginator(requerimento, 10)
        page = request.GET.get('page')
        try:
            requerimento = paginator.page(page)
        except PageNotAnInteger:
            requerimento = paginator.page(1)
        except EmptyPage:
            requerimento = paginator.page(paginator.num_pages)
        dados = {'requerimento': requerimento, 'criterio': criterio, 'paginator': paginator, 'page_obj': requerimento,
                 "tipo_requerimento": tipo_requerimento, "professores": professores, "disciplinas": disciplinas,
                 'requerimentos_professor': requerimentos_professor}
        return render(request, 'req/req_list_indeferidos.html', dados)

    # TECNICO ADMINISTRATIVO
    elif (tecnico != None):
        if (criterio):
            requerimento = Requerimento.objects.filter(encaminhado_para=None, situacao=3,
                                                       aluno__pessoa__nome__contains=criterio).order_by(
                'tipo_requerimento', 'data_solicitacao_requerimento')

        if (criterio_prof):
            requerimento = Requerimento.objects.filter(encaminhado_para=None, situacao=3,
                                                       professor_atividade__pessoa__nome__contains=criterio_prof).order_by('data_solicitacao_requerimento', 'aluno__pessoa__nome')
        if (criterio_disciplina):
            requerimento = Requerimento.objects.filter(encaminhado_para=None, situacao=3,
                                                       disciplina__disciplina__nome__contains=criterio_disciplina).order_by(
                'data_solicitacao_requerimento', 'aluno__pessoa__nome')

        if (criterio_prof or criterio or criterio_disciplina):
            requerimento = Requerimento.objects.filter(encaminhado_para=None, situacao=3,
                                                       professor_atividade__pessoa__nome__contains=criterio_prof
                                                       ,aluno__pessoa__nome__contains=criterio,
                                                       disciplina__disciplina__nome__contains=criterio_disciplina).order_by \
                ('data_solicitacao_requerimento', 'aluno__pessoa__nome')


        else:
            requerimento = Requerimento.objects.all().filter(encaminhado_para=None, situacao=3).order_by(
                'data_solicitacao_requerimento', 'aluno__pessoa__nome')
            criterio = ""
        # Cria o mecanimos de paginação
        paginator = Paginator(requerimento, 10)
        page = request.GET.get('page')
        try:
            requerimento = paginator.page(page)
        except PageNotAnInteger:
            requerimento = paginator.page(1)
        except EmptyPage:
            requerimento = paginator.page(paginator.num_pages)
        dados = {'requerimento': requerimento, 'criterio': criterio, 'paginator': paginator, 'page_obj': requerimento,
                 "tipo_requerimento": tipo_requerimento, "professores": professores, "disciplinas": disciplinas,
                 'requerimentos_professor': requerimentos_professor}
        return render(request, 'req/req_list_indeferidos.html', dados)

@login_required(login_url='login')
@permission_required('appsgr.add_tipo_requerimento',login_url='erro_permissao')
def req_autenticado(request):
    criterio = request.GET.get('criterio')
    pessoa_logada = User.objects.get(username=request.user.username)
    tipo_requerimento = TipoRequerimento.objects.all().order_by('nome')
    professores = Professor.objects.all().order_by('pessoa__nome')
    disciplinas = Disciplina.objects.all().order_by('nome')
    requerimentos_professor = []

    # Instanciando objetos
    try:
        coordenador = Coordenador.objects.get(username=pessoa_logada.username)
    except Coordenador.DoesNotExist:
        coordenador = None
    try:
        professor = Professor.objects.get(username=pessoa_logada.username)
    except Professor.DoesNotExist:
        professor = None
    try:
        tecadm = Tecnico_Administrativo.objects.get(username=pessoa_logada.username)
    except Tecnico_Administrativo.DoesNotExist:
        tecadm = None


    # COORDENADOR
    if (coordenador != None):
        if (criterio):
            requerimento = Requerimento.objects.all().filter(codigo=criterio)
        else:
            requerimento = ""
            criterio = ""
        dados = {'requerimento': requerimento, 'criterio': criterio,
                 "tipo_requerimento": tipo_requerimento, "professores": professores, "disciplinas": disciplinas,
                 'requerimentos_professor': requerimentos_professor}
        return render(request, 'req/req_autenticado.html', dados)

    # PROFESSOR
    if (professor != None):
        if (criterio):
            requerimento = Requerimento.objects.all().filter(codigo=criterio)
        else:
            requerimento = ""
            criterio = ""
        dados = {'requerimento': requerimento, 'criterio': criterio,
                 "tipo_requerimento": tipo_requerimento, "professores": professores, "disciplinas": disciplinas,
                 'requerimentos_professor': requerimentos_professor}
        return render(request, 'req/req_autenticado.html', dados)

    # TEC ADM
    if (tecadm != None):
        if (criterio):
            requerimento = Requerimento.objects.all().filter(codigo=criterio)
        else:
            requerimento = ""
            criterio = ""
        dados = {'requerimento': requerimento, 'criterio': criterio,
                 "tipo_requerimento": tipo_requerimento, "professores": professores, "disciplinas": disciplinas,
                 'requerimentos_professor': requerimentos_professor}
        return render(request, 'req/req_autenticado.html', dados)
