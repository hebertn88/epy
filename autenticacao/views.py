from urllib import request
from django.contrib import messages, auth
from django.contrib.messages import constants
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render



# Create your views here.
def cadastro(request):
    if not request.user.is_authenticated:
        return redirect('/auth/login')

    if request.method == 'GET':
        return render(request, 'cadastro.html')

    elif request.method == 'POST':
        nome_usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        confirma_senha = request.POST.get('confirma_senha')

        if User.objects.filter(username=nome_usuario):
            messages.add_message(request, constants.ERROR, 'Usuário já existe.')
            return render(request, 'cadastro.html')
        
        if senha != confirma_senha:
            messages.add_message(request, constants.ERROR, 'Você digitou senhas diferentes.')
            return render(request, 'cadastro.html')
    
        try:
            usuario = User.objects.create_user(username=nome_usuario,
            password=senha)
            usuario.save()
            messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso.')
            return redirect('/auth/login')
        except:
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
            return render(request, 'login.html')
        else:
            if not User.objects.filter(username=nome_usuario):
                messages.add_message(request, constants.ERROR, 'Usuário não encontrado.')
            else:
                messages.add_message(request, constants.ERROR, 'Senha inválida.')
                                
            return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

