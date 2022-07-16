from audioop import reverse
from multiprocessing import context
from django.db.models import Q
from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import redirect, render
from .models import Funcionario
from setor.models import Setor

# Create your views here.

def cadastro(request):
    #verifica se usuario esta autenticado
    if not request.user.is_authenticated:
        return redirect('/auth/login')

    setores = Setor.objects.all().order_by('descricao')
    context = {'setores': setores}

    if request.method == 'GET':
        return render(request, 'cadastro_funcionario.html', context)
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        setor = request.POST.get('setor')
        ativo = request.POST.get('ativo')

        if not ativo:
            ativo = False

        if nome == '' or sobrenome == '':
            messages.add_message(request, constants.ERROR, 'Nome e Sobrenome devem ser preenchidos.')
            return redirect('/funcionario/cadastro')

        #verifica se existe funcionario com mesmo nome e sobrenome
        if Funcionario.objects.filter(Q(nome=nome) & Q(sobrenome=sobrenome)):
            messages.add_message(request, constants.ERROR, 'Já existe um funcionário com o mesmo Nome e Sobrenome.')
            return redirect('/funcionario/cadastro')

        #verifica se setor informado existe
        try:
            setor = Setor.objects.get(pk=setor)
        except:
            messages.add_message(request, constants.ERROR, 'Setor não existe.')
            return redirect('/funcionario/cadastro')            
        
        #grava novo registro
        try:
            Funcionario.objects.create(nome=nome, sobrenome=sobrenome, setor=setor, ativo=ativo)
            messages.add_message(request, constants.SUCCESS, 'Setor cadastrado com sucesso.')

            return redirect('/funcionario')
        except Exception as e:
            #se erro
            messages.add_message(request, constants.ERROR, f'Erro ao cadastrar Funcionario.')
            return redirect('/funcionario/cadastro')


def edicao(request, id):
    #verifica se usuario esta autenticado
    if not request.user.is_authenticated:
        return redirect('/auth/login')
    
    try:
        funcionario =  Funcionario.objects.get(pk=id)
        setores = Setor.objects.all().order_by('descricao')
        context = {
            'funcionario': funcionario,
            'setores': setores}
    except:
        messages.add_message(request, constants.ERROR, 'Funcionário não encontrado.')
        return redirect('/funcionario/')
    
    if request.method == 'GET':
        return render(request, 'edicao_funcionario.html', context)
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        setor = request.POST.get('setor')
        ativo = request.POST.get('ativo')
        print(ativo)
        if not ativo:
            ativo = False
            print(ativo)

        #verifica se existe funcionario com mesmo nome e sobrenome
        if Funcionario.objects.filter(Q(nome=nome) & Q(sobrenome=sobrenome)):
            func_existente = Funcionario.objects.get(Q(nome=nome) & Q(sobrenome=sobrenome))
            if func_existente.id != id:
                messages.add_message(request, constants.ERROR, 'Já existe um funcionário com o mesmo Nome e Sobrenome.')
                return redirect(f'/funcionario/edicao/{funcionario.id}')
        
        try:
            setor = Setor.objects.get(pk=setor)
        except:
            messages.add_message(request, constants.ERROR, 'Setor inválido.')
            return redirect(f'/funcionario/edicao/{funcionario.id}')

        try:
            funcionario.nome = nome
            funcionario.sobrenome = sobrenome
            funcionario.setor = setor
            funcionario.ativo = ativo

            funcionario.save()
            messages.add_message(request, constants.SUCCESS, 'Funcionário alterado com sucesso.')
            return redirect('/funcionario/')
        except:
            messages.add_message(request, constants.ERROR, 'Não foi possível alterar o funcionário.')
            return redirect('/funcionario/')

        


def funcionarios(request):
    #verifica se usuario esta autenticado
    if not request.user.is_authenticated:
        return redirect('/auth/login')

    funcionarios = Funcionario.objects.all().order_by('-ativo', 'setor__descricao', 'nome')
    context = {'funcionarios': funcionarios}
    return render(request, 'funcionarios.html', context)


def exclusao(request, id):
    #verifica se usuario esta autenticado
    if not request.user.is_authenticated:
        return redirect('/auth/login')
    
    try:
        funcionario =  Funcionario.objects.get(pk=id)
        context = {'funcionario': funcionario}
    except:
        messages.add_message(request, constants.ERROR, 'Funcionário não encontrado.')
        return redirect('/funcionario/')
    
    if request.method == 'GET':
        return render(request, 'exclusao_funcionario.html', context)
    elif request.method == 'POST':
        
        try:
            #exclui registro
            funcionario.delete()
            messages.add_message(request, constants.SUCCESS, 'Funcionário excluído com sucesso.')
            return redirect('/funcionario/')
        except:
            #se erro ao exlcuir
            messages.add_message(request, constants.ERROR, 'Não foi possível excluir o Funcionário.')
            return redirect(f'/funcionario/{funcionario.id}')
    

    