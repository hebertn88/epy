import re
from django.contrib import messages
from django.contrib.messages import constants


def valida_senha(request, senha, confirma_senha):
    if len(senha) < 6:
        messages.add_message(request, constants.ERROR, 'Sua senha deve conter 6 ou mais caractertes.')
        return False
    if not senha == confirma_senha:
        messages.add_message(request, constants.ERROR, 'As senhas não coincidem!')
        return False
    if not (re.search('[A-Z]', senha.upper()) and re.search('[1-9]', senha)):
        messages.add_message(request, constants.ERROR, 'Sua senha deve conter números e letras')
        return False

    return True

