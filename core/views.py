from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect
from core.models import Evento
from django.contrib.auth.decorators import  login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from datetime import datetime
from django.http.response import Http404, JsonResponse


# Create your views here.
def index(request):
    return redirect('/agenda')

def evento(request,evento):
    data = Evento.objects.get(titulo=evento)
    return HttpResponse("<h1>Evento: </h1>{} <h1>Local: </h1>{}".format(data.titulo,data.local))

@login_required(login_url='/login')
def lista_eventos(request):
    #eventos = Evento.objects.all()
    usuario = request.user
    data_atual = datetime.now()
    eventos = Evento.objects.filter(usuario=usuario)
    # eventos = Evento.objects.filter(usuario=usuario,
    #                                 data_evento__gt=data_atual)
    data = {
        'eventos':eventos
    }
    return render(request,'agenda.html',data)

def login_user(request):
    return render(request,'login.html')

def submit_login(request):
    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        usuario = authenticate(username=username,password=password)
        if usuario is not None:
            login(request,usuario)
            return redirect('/')
        else:
            messages.error(request, "Usuário ou senha inválida")
            return redirect('/login')
    else:
        return redirect('/login')

def logout_user(request):
    logout(request)
    return redirect('/login')

@login_required(login_url='/login')
def evento(request):
    id_evento = request.GET.get("id")
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request,'evento.html', dados)

@login_required(login_url='/login')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get("titulo")
        data = request.POST.get("data")
        descricao = request.POST.get("descricao")
        local = request.POST.get("local")
        usuario = request.user
        id_evento = request.POST.get("id_evento")
        if id_evento:
            evento = Evento.objects.get(id=id_evento)
            if evento.usuario == usuario:
                evento.titulo = titulo
                evento.data_evento=data
                evento.descricao=descricao
                evento.local=local
                evento.save()
            # Evento.objects.filter(id=id_evento).update(titulo=titulo,
            #                                           data_evento=data,
            #                                           descricao=descricao,
            #                                           local=local)
        else:
            Evento.objects.create(
                titulo=titulo,
                data_evento=data,
                descricao=descricao,
                usuario=usuario,
                local=local
            )
    return redirect('/')

@login_required(login_url='/login')
def delete_evento(request,id):
    usuario = request.user
    try:
        evento = Evento.objects.get(id=id)
    except Exception:
        raise Http404()
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404()
    return redirect('/')

@login_required(login_url='/login')
def json_lista_eventos(request,id_usuario):
    usuario = User.objects.get(id=id_usuario)
    eventos = Evento.objects.filter(usuario=usuario).values('id','titulo','data_evento','descricao')

    return JsonResponse(list(eventos),safe=False)