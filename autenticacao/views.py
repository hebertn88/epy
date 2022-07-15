from django.contrib import messages, auth
from django.contrib.messages import constants
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .utils import valida_senha


# Create your views here.
def altera_senha(request, id):
    if not request.user.is_authenticated:
        return redirect('/auth/login')
    
    usuario = User.objects.get(pk=id)

    if not usuario:
        messages.add_message(request, constants.ERROR, 'Usuário não encontrado.')
        return redirect('/auth/cadastro')
    
    if request.method == 'GET':
        return render(request, 'altera_senha.html')
    elif request.method == 'POST':
        senha_atual = request.POST.get('senha_atual')
        senha = request.POST.get('senha')
        confirma_senha = request.POST.get('confirma_senha')

        if authenticate(username=usuario.username, password=senha_atual):
            if not valida_senha(request, senha, confirma_senha):
                return redirect(f'/auth/altera_senha/{usuario.id}') 
            try:
                usuario.set_password(senha)
                usuario.save()
                messages.add_message(request, constants.SUCCESS, 'Senha alterada com sucesso.')
                return redirect('/auth/cadastro')
            except:
                messages.add_message(request, constants.ERROR, 'Não foi possível alterar a senha.')
                return redirect(f'/auth/altera_senha/{usuario.id}')
        else:
            messages.add_message(request, constants.ERROR, 'Senha atual inválida.')
            return redirect(f'/auth/altera_senha/{usuario.id}')


def cadastro(request):
    if not request.user.is_authenticated:
        return redirect('/auth/login')

    if request.method == 'GET':
        return render(request, 'cadastro_usuario.html')
    elif request.method == 'POST':
        nome_usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        confirma_senha = request.POST.get('confirma_senha')

        if User.objects.filter(username=nome_usuario):
            messages.add_message(request, constants.ERROR, 'Usuário já existe.')
            return render(request, 'cadastro_usuario.html')
        
        if not valida_senha(request, senha, confirma_senha):
            return render(request, 'cadastro_usuario.html')
    
        try:
            usuario = User.objects.create_user(username=nome_usuario,
            password=senha)
            usuario.save()
            auth.login(request, usuario)
            messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso.')
            return redirect('/auth/cadastro')
        except:
            messages.add_message(request, constants.ERROR, 'Não foi possível alterar a senha.')
            return redirect('/auth/cadastro')



def login(request):
    if request.user.is_authenticated:
        return HttpResponse('já autenticado')

    if request.method == 'GET':
        return render(request, 'login.html')

    elif request.method == 'POST':
        nome_usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')

        usuario = authenticate(username=nome_usuario, password=senha)

        if usuario is not None:
            messages.add_message(request, constants.SUCCESS, 'Usuário autenticado.')
            auth.login(request, usuario)
            return redirect('/auth/cadastro')
        else:
            if not User.objects.filter(username=nome_usuario):
                messages.add_message(request, constants.ERROR, 'Usuário não encontrado.')
            else:
                messages.add_message(request, constants.ERROR, 'Senha inválida.')
                                
            return redirect('/auth/login')

def logout(request):
    auth.logout(request)
    return redirect('/')

