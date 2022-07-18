from urllib import request
from django.contrib import messages
from django.contrib.messages import constants
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Setor

# Create your views here.
def cadastro(request):
    #verifica se usuario esta autenticado
    if not request.user.is_authenticated:
        return redirect('/auth/login')
    
    if request.method == 'GET':
        return render(request, 'cadastro_setor.html')
    elif request.method =='POST':
        descricao = request.POST.get('descricao')
    
        #verifica se ja existe setor com mesma descricao
        if Setor.objects.filter(descricao=descricao):
            messages.add_message(request, constants.ERROR, 'Setor já existe.')
            return redirect('/setor/cadastro')

        try:
            #grava novo registro
            Setor.objects.create(descricao=descricao)
            messages.add_message(request, constants.SUCCESS, 'Setor cadastrado com sucesso.')
            return redirect('/setor')
        except:
            #se erro
            messages.add_message(request, constants.ERROR, 'Erro ao cadastrar Setor.')
            return redirect('/setor/cadastro')


def edicao(request, id):
    #verifica se usuario esta autenticado    
    if not request.user.is_authenticated:
        return redirect('/auth/login')

    #busca setor, se nao existir redireciona
    setor = Setor.objects.get(pk=id)
    if not setor:
        messages.add_message(request, constants.ERROR, 'Setor não encontrado.')
        return redirect('/setor/')

    context = {'setor': setor}

    if request.method == 'GET':
        return render(request, 'edicao_setor.html', context)
    elif request.method == 'POST':
        descricao = request.POST.get('descricao')

        #verifica se ja existe setor com nova descricao
        if Setor.objects.filter(descricao=descricao):
            messages.add_message(request, constants.ERROR, 'Já existe um Setor com esta descrição.')
            return redirect(f'/setor/edicao/{id}')

        try:
            #altera e grava alteracao
            setor.descricao = descricao
            setor.save()
            messages.add_message(request, constants.SUCCESS, 'Setor alterado com sucesso.')

            return redirect('/setor')
        except:
            #se erro
            messages.add_message(request, constants.ERROR, 'Não foi possível realizar a alteração.')

            return redirect(f'/setor/edicao/{id}')


def exclusao(request, id):
    #verifica se usuario esta autenticado
    if not request.user.is_authenticated:
        return redirect('/auth/login')

    #busca setor, se nao existir redireciona
    try:
        setor = Setor.objects.get(pk=id)
        context = {'setor': setor}    
    except:
        messages.add_message(request, constants.ERROR, 'Setor não encontrado.')
        return redirect('/setor/')

    if request.method == 'GET':
        return render(request, 'exclusao_setor.html', context)
    elif request.method == 'POST':
        try:
            #exclui registro
            setor.delete()
            messages.add_message(request, constants.SUCCESS, 'Setor excluído com sucesso.')
            return redirect('/setor/')
        except:
            #se erro ao exlcuir
            messages.add_message(request, constants.ERROR, 'Não foi possível excluir o Setor.')
            return redirect('/setor/')


def setores(request):
    #verifica se usuario esta autenticado    
    if not request.user.is_authenticated:
        return redirect('/auth/login')

    #busca todos setores ordenados por descricao
    setores = Setor.objects.all().order_by('descricao')
    context = {'setores': setores}
    return render(request, 'setores.html', context)

