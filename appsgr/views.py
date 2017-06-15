from django.contrib.auth.decorators import login_required,permission_required
from django.shortcuts import render,redirect
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from appssgr.forms import *
from django.forms import modelform_factory

# Create your views here..

@login_required(login_url='login')
def home(request):
   return render(request,'base.html')

@login_required(login_url='login')
def curso(request):
    return render(request,'curso.html')

@login_required(login_url='login')
def erro_permissao(request):
    return render(request,'req/erro_permissao.html')

@permission_required('appssgr.add_requerimento',login_url='erro_permissao')
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
            return redirect('req_list')
    else:
        form=RequerimentoFormNovo()
    dados={'form':form}
    return render(request, 'req/req_form.html', dados)

@permission_required('appssgr.add_requerimento',login_url='erro_permissao')
def req_list(request):
    criterio=request.GET.get('criterio')
    pessoa_logada = Pessoa.objects.get(username=request.user.username)
    tipo_requerimento=TipoRequerimento.objects.all().order_by('nome')
    requerimentos_professor = []

    #Instanciando objetos
    try:
        aluno = Aluno.objects.get(username=pessoa_logada.username)
    except Aluno.DoesNotExist:
        aluno = None
    try:
        professor = Professor.objects.get(pessoa_id=pessoa_logada.id)
    except Professor.DoesNotExist:
        professor = None
    try:
        tecnico = Tecnico_Administrativo.objects.get(pessoa_id=pessoa_logada.id)
    except Tecnico_Administrativo.DoesNotExist:
        tecnico = None

    #ALUNO
    if(aluno != None):
        if (criterio):
            requerimento=Requerimento.objects.filter(situacao=1,tipo_requerimento__nome__contains=criterio, aluno=aluno).order_by('tipo_requerimento','-data_solicitacao_requerimento')
        else:
            requerimento=Requerimento.objects.filter(situacao=1,aluno_id=aluno).order_by('tipo_requerimento','-data_solicitacao_requerimento') #| Requerimento.objects.filter(tipo_requerimento_id=2).order_by('tipo_requerimento','-data_solicitacao_requerimento')
            criterio=""
        #Cria o mecanimos de paginação
        paginator=Paginator(requerimento,10)
        page=request.GET.get('page')
        try:
            requerimento=paginator.page(page)
        except PageNotAnInteger:
            requerimento=paginator.page(1)
        except EmptyPage:
            requerimento=paginator.page(paginator.num_pages)
        dados={'requerimento':requerimento,'criterio':criterio,'paginator':paginator,'page_obj':requerimento, "tipo_requerimento":tipo_requerimento}
        return render(request, 'req/req_criar.html', dados)
    # PROFESSOR
    elif(professor != None):
        if (criterio):
            requerimento=Requerimento.objects.filter(encaminhado_para=pessoa_logada,situacao=1,tipo_requerimento__nome__contains=criterio).order_by('tipo_requerimento','data_solicitacao_requerimento')
        else:
            requerimento=Requerimento.objects.all().filter(encaminhado_para=pessoa_logada,situacao=1).order_by('tipo_requerimento','data_solicitacao_requerimento')
            criterio=""
        #Cria o mecanimos de paginação
        paginator=Paginator(requerimento,10)
        page=request.GET.get('page')
        try:
            requerimento=paginator.page(page)
        except PageNotAnInteger:
            requerimento=paginator.page(1)
        except EmptyPage:
            requerimento=paginator.page(paginator.num_pages)
        dados={'requerimento':requerimento,'criterio':criterio,'paginator':paginator,'page_obj':requerimento, "tipo_requerimento":tipo_requerimento, 'requerimentos_professor':requerimentos_professor}
        return render(request, 'req/req_list_prof.html', dados)

    # TECNICO ADMINISTRATIVO
    elif (tecnico != None):
        if (criterio):
            requerimento = Requerimento.objects.filter(encaminhado_para=None, situacao=1,descricao__contains=criterio).order_by('tipo_requerimento',
                                                                                       '-data_solicitacao_requerimento')
        else:
            requerimento = Requerimento.objects.filter(encaminhado_para=None, situacao=1).order_by('tipo_requerimento',
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
        dados = {'requerimento': requerimento, 'criterio': criterio, 'paginator': paginator, 'page_obj': requerimento,
                 "tipo_requerimento": tipo_requerimento, 'requerimentos_professor': requerimentos_professor}
        return render(request, 'req/req_list_tecnico.html', dados)

@permission_required('appssgr.view_requerimento',login_url='erro_permissao')
def req_list_avaliacao(request):
    criterio=request.GET.get('criterio')
    pessoa_logada = Pessoa.objects.get(username=request.user.username)
    tipo_requerimento=TipoRequerimento.objects.all().order_by('nome')
    requerimentos_professor = []

    #Instanciando objetos
    try:
        aluno = Aluno.objects.get(username=pessoa_logada.username)
    except Aluno.DoesNotExist:
        aluno = None
    try:
        professor = Professor.objects.get(pessoa_id=pessoa_logada.id)
    except Professor.DoesNotExist:
        professor = None
    try:
        tecnico = Tecnico_Administrativo.objects.get(pessoa_id=pessoa_logada.id)
    except Tecnico_Administrativo.DoesNotExist:
        tecnico = None

    #ALUNO
    if(aluno != None):
        if (criterio):
            requerimento=Requerimento.objects.filter(situacao=1,tipo_requerimento__nome__contains=criterio, aluno=aluno).order_by('tipo_requerimento','-data_solicitacao_requerimento')
        else:
            requerimento=Requerimento.objects.filter(situacao=1,aluno_id=aluno).order_by('tipo_requerimento','-data_solicitacao_requerimento') #| Requerimento.objects.filter(tipo_requerimento_id=2).order_by('tipo_requerimento','-data_solicitacao_requerimento')
            criterio=""
        #Cria o mecanimos de paginação
        paginator=Paginator(requerimento,10)
        page=request.GET.get('page')
        try:
            requerimento=paginator.page(page)
        except PageNotAnInteger:
            requerimento=paginator.page(1)
        except EmptyPage:
            requerimento=paginator.page(paginator.num_pages)
        dados={'requerimento':requerimento,'criterio':criterio,'paginator':paginator,'page_obj':requerimento, "tipo_requerimento":tipo_requerimento}
        return render(request, 'req/req_list_aluno.html', dados)
    # PROFESSOR
    elif(professor != None):
        if (criterio):
            requerimento=Requerimento.objects.filter(encaminhado_para=pessoa_logada,situacao=1,tipo_requerimento__nome__contains=criterio).order_by('tipo_requerimento','data_solicitacao_requerimento')
        else:
            requerimento=Requerimento.objects.all().filter(encaminhado_para=pessoa_logada,situacao=1).order_by('tipo_requerimento','data_solicitacao_requerimento')
            criterio=""
        #Cria o mecanimos de paginação
        paginator=Paginator(requerimento,10)
        page=request.GET.get('page')
        try:
            requerimento=paginator.page(page)
        except PageNotAnInteger:
            requerimento=paginator.page(1)
        except EmptyPage:
            requerimento=paginator.page(paginator.num_pages)
        dados={'requerimento':requerimento,'criterio':criterio,'paginator':paginator,'page_obj':requerimento, "tipo_requerimento":tipo_requerimento, 'requerimentos_professor':requerimentos_professor}
        return render(request, 'req/req_list_prof.html', dados)

    # TECNICO ADMINISTRATIVO
    elif (tecnico != None):
        if (criterio):
            requerimento = Requerimento.objects.filter(encaminhado_para=None, situacao=1,descricao__contains=criterio).order_by('tipo_requerimento',
                                                                                       '-data_solicitacao_requerimento')
        else:
            requerimento = Requerimento.objects.filter(encaminhado_para=None, situacao=1).order_by('tipo_requerimento',
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
        dados = {'requerimento': requerimento, 'criterio': criterio, 'paginator': paginator, 'page_obj': requerimento,
                 "tipo_requerimento": tipo_requerimento, 'requerimentos_professor': requerimentos_professor}
        return render(request, 'req/req_list_tecnico.html', dados)

@permission_required('appssgr.detail_requerimento',login_url='erro_permissao')
def req_detail(request, pk):
    pessoa_logada = Pessoa.objects.get(username=request.user.username)
    usuarios = []
    request.session[0]=pk
    try:
        aluno = Aluno.objects.get(username=pessoa_logada.username)
    except Aluno.DoesNotExist:
        aluno = None
    try:
        professor = Professor.objects.get(pessoa_id=pessoa_logada.id)
    except Professor.DoesNotExist:
        professor = None
    try:
        tecnico = Tecnico_Administrativo.objects.get(pessoa_id=pessoa_logada.id)
    except Tecnico_Administrativo.DoesNotExist:
        tecnico = None

    requerimento=Requerimento.objects.get(id=pk)
    form=RequerimentoForm(request.POST,instance=requerimento)
    dados = {'form':form,'usuarios':usuarios,'requerimento':requerimento}
    return render(request, 'req/req_detail.html', dados)

@permission_required('appssgr.change_requerimento',login_url='erro_permissao')
def req_update(request,pk):
    requerimento=Requerimento.objects.get(id=pk)
    if (request.method=="POST"):
        form=RequerimentoForm(request.POST,request.FILES,instance=requerimento)
        if (form.is_valid()):
            form.save()
            return redirect('home')
    else:
        form=RequerimentoForm(instance=requerimento)
        dados={'form':form}
        return render(request, 'req/req_form.html', dados)

##############

@permission_required('appssgr.view_tipo_requerimento',login_url='erro_permissao')
def req_list_deferidos(request):
    criterio=request.GET.get('criterio')
    pessoa_logada = Pessoa.objects.get(username=request.user.username)
    tipo_requerimento=TipoRequerimento.objects.all().order_by('nome')
    requerimentos_professor = []

    #Instanciando objetos
    try:
        aluno = Aluno.objects.get(username=pessoa_logada.username)
    except Aluno.DoesNotExist:
        aluno = None
    try:
        professor = Professor.objects.get(pessoa_id=pessoa_logada.id)
    except Professor.DoesNotExist:
        professor = None
    #ALUNO
    if(aluno != None):
        if (criterio):
            requerimento=Requerimento.objects.filter(situacao=2,tipo_requerimento__nome__contains=criterio, aluno=aluno).order_by('tipo_requerimento','-data_solicitacao_requerimento')
        else:
            requerimento=Requerimento.objects.filter(situacao=2,aluno_id=aluno).order_by('tipo_requerimento','-data_solicitacao_requerimento') #| Requerimento.objects.filter(tipo_requerimento_id=2).order_by('tipo_requerimento','-data_solicitacao_requerimento')
            criterio=""
        #Cria o mecanimos de paginação
        paginator=Paginator(requerimento,10)
        page=request.GET.get('page')
        try:
            requerimento=paginator.page(page)
        except PageNotAnInteger:
            requerimento=paginator.page(1)
        except EmptyPage:
            requerimento=paginator.page(paginator.num_pages)
        dados={'requerimento':requerimento,'criterio':criterio,'paginator':paginator,'page_obj':requerimento, "tipo_requerimento":tipo_requerimento}
        return render(request, 'req/req_list_deferidos_alunos.html', dados)
    # PROFESSOR
    elif(professor != None):
        if (criterio):
            requerimento=Requerimento.objects.filter(situacao=2,tipo_requerimento__nome__contains=criterio, encaminhado_para=pessoa_logada).order_by('tipo_requerimento','data_solicitacao_requerimento')
        else:
            requerimento=Requerimento.objects.all().filter(situacao=2,encaminhado_para=pessoa_logada).order_by('tipo_requerimento','data_solicitacao_requerimento')
            criterio=""
        #Cria o mecanimos de paginação
        paginator=Paginator(requerimento,10)
        page=request.GET.get('page')
        try:
            requerimento=paginator.page(page)
        except PageNotAnInteger:
            requerimento=paginator.page(1)
        except EmptyPage:
            requerimento=paginator.page(paginator.num_pages)
        dados={'requerimento':requerimento,'criterio':criterio,'paginator':paginator,'page_obj':requerimento, "tipo_requerimento":tipo_requerimento, 'requerimentos_professor':requerimentos_professor}
        return render(request, 'req/req_list_deferidos_prof.html', dados)

@permission_required('appssgr.view_requerimento',login_url='erro_permissao')
def req_list_indeferidos(request):
    criterio=request.GET.get('criterio')
    pessoa_logada = Pessoa.objects.get(username=request.user.username)
    tipo_requerimento=TipoRequerimento.objects.all().order_by('nome')
    requerimentos_professor = []

    #Instanciando objetos
    try:
        aluno = Aluno.objects.get(username=pessoa_logada.username)
    except Aluno.DoesNotExist:
        aluno = None
    try:
        professor = Professor.objects.get(pessoa_id=pessoa_logada.id)
    except Professor.DoesNotExist:
        professor = None
    try:
        tecnico = Tecnico_Administrativo.objects.get(pessoa_id=pessoa_logada.id)
    except Tecnico_Administrativo.DoesNotExist:
        tecnico = None

    #ALUNO
    if(aluno != None):
        if (criterio):
            requerimento=Requerimento.objects.filter(situacao=3,tipo_requerimento__nome__contains=criterio, aluno=aluno).order_by('tipo_requerimento','-data_solicitacao_requerimento')
        else:
            requerimento=Requerimento.objects.filter(situacao=3,aluno_id=aluno).order_by('tipo_requerimento','-data_solicitacao_requerimento') #| Requerimento.objects.filter(tipo_requerimento_id=2).order_by('tipo_requerimento','-data_solicitacao_requerimento')
            criterio=""
        #Cria o mecanimos de paginação
        paginator=Paginator(requerimento,10)
        page=request.GET.get('page')
        try:
            requerimento=paginator.page(page)
        except PageNotAnInteger:
            requerimento=paginator.page(1)
        except EmptyPage:
            requerimento=paginator.page(paginator.num_pages)
        dados={'requerimento':requerimento,'criterio':criterio,'paginator':paginator,'page_obj':requerimento, "tipo_requerimento":tipo_requerimento}
        return render(request, 'req/req_list_indeferidos_alunos.html', dados)
    # PROFESSOR
    elif(professor != None):
        if (criterio):
            requerimento=Requerimento.objects.filter(situacao=3,tipo_requerimento__nome__contains=criterio, encaminhado_para=pessoa_logada).order_by('tipo_requerimento','data_solicitacao_requerimento')
        else:
            requerimento=Requerimento.objects.all().filter(situacao=3,encaminhado_para=pessoa_logada).order_by('tipo_requerimento','data_solicitacao_requerimento')
            criterio=""
        #Cria o mecanimos de paginação
        paginator=Paginator(requerimento,10)
        page=request.GET.get('page')
        try:
            requerimento=paginator.page(page)
        except PageNotAnInteger:
            requerimento=paginator.page(1)
        except EmptyPage:
            requerimento=paginator.page(paginator.num_pages)
        dados={'requerimento':requerimento,'criterio':criterio,'paginator':paginator,'page_obj':requerimento, "tipo_requerimento":tipo_requerimento, 'requerimentos_professor':requerimentos_professor}
        return render(request, 'req/req_list_indeferidos_prof.html', dados)
    elif (tecnico != None):
        if (criterio):
            requerimento = Requerimento.objects.filter(situacao=3, tipo_requerimento__nome__contains=criterio,
                                                       encaminhado_para=None).order_by('tipo_requerimento',
                                                                                                'data_solicitacao_requerimento')
        else:
            requerimento = Requerimento.objects.all().filter(situacao=3,encaminhado_para=None).order_by(
                'tipo_requerimento', 'data_solicitacao_requerimento')
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
                 "tipo_requerimento": tipo_requerimento, 'requerimentos_professor': requerimentos_professor}
        return render(request, 'req/req_list_indeferidos_tecnico.html', dados)