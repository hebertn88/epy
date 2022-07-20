from multiprocessing import context
from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import redirect, render
from .models import Equipamento, EquipamentoSetor
from setor.models import Setor

# Create your views here.
def cadastro(request):
    #verifica se usuario esta autenticado
    if not request.user.is_authenticated:
        return redirect('/auth/login')

    try:
        setores = Setor.objects.all().order_by('descricao')
        context = {'setores': setores}
    except:
        messages.add_message(request, constants.ERROR, 'Erro ao carrregar setores.')
        return redirect('/equipamento/')

    if request.method == 'GET':
        return render(request, 'cadastro_equipamento.html', context)
    elif request.method == 'POST':
        descricao = request.POST.get('descricao')
        setor = request.POST.get('setor')
        validade = request.POST.get('validade')

        if Equipamento.objects.filter(descricao=descricao):
            messages.add_message(request, constants.ERROR, 'Já existe um equipamento com esta descrição.')
            return redirect('/equipamento/cadastro')

        try:
            setor = Setor.objects.get(pk=setor)
        except:
            messages.add_message(request, constants.ERROR, 'Setor inválido.')
            return redirect('/equipamento/cadastro')

        try:
            equipamento = Equipamento.objects.create(descricao=descricao)
            EquipamentoSetor.objects.create(equipamento=equipamento, setor=setor, validade=validade)
            messages.add_message(request, constants.SUCCESS, 'Equipamento cadastrado com sucesso.')

            return redirect('/equipamento/')
        except:
            messages.add_message(request, constants.ERROR, 'Erro ao cadastrar equipamento.')

            return redirect('/equipamento/')


def edicao(request, id):
    #verifica se usuario esta autenticado
    if not request.user.is_authenticated:
        return redirect('/auth/login')
    
    try:
        equipamento = Equipamento.objects.get(pk=id)
        context = {'equipamento': equipamento}
    except:
        messages.add_message(request, constants.ERROR, 'Erro ao carrregar Equipamento.')
        return redirect('/equipamento/')

    if request.method == 'GET':
        return render(request, 'edicao_equipamento.html', context)
    elif request.method == 'POST':
        descricao = request.POST.get('descricao')
        equipamento_existente = Equipamento.objects.filter(descricao=descricao)
        print(equipamento_existente)
        if equipamento_existente:
            if equipamento_existente[0].id != equipamento.id:
                messages.add_message(request, constants.ERROR, 'Já existe um Equipamento com a mesma descrição')
                return redirect(f'/equipamento/edicao/{id}')
            else:
                messages.add_message(request, constants.INFO, 'Nenhuma alteração foi realizada.')
                return redirect(f'/equipamento/edicao/{id}')
        equipamento.descricao = descricao
        equipamento.save()
        messages.add_message(request, constants.SUCCESS, 'Alteração realizada com sucesso.')
        return redirect('/equipamento/')

    
def equipamentos(request):
    #verifica se usuario esta autenticado
    if not request.user.is_authenticated:
        return redirect('/auth/login')

    equipamentos = Equipamento.objects.all().order_by('descricao')
    context = {'equipamentos': equipamentos}
    return render(request, 'equipamentos.html', context)

def exclusao(request, id):
    #verifica se usuario esta autenticado
    if not request.user.is_authenticated:
        return redirect('/auth/login')

    try:
        equipamento = Equipamento.objects.get(pk=id)
        context = {'equipamento': equipamento}
    except:
        messages.add_message(request, constants.ERROR, 'Equipamento inválido.')
        return redirect('/equipamento/')
    
    if request.method == 'GET':
        return render(request, 'exclusao_equipamento.html', context)
    elif request.method == 'POST':
        try:
            equipamento.delete()
            messages.add_message(request, constants.SUCCESS, 'Equipamento excluído com sucesso.')
            return redirect('/equipamento/')
        except:
            #se erro ao exlcuir
            messages.add_message(request, constants.ERROR, 'Não foi possível excluir o Equipamento.')
            return redirect(f'/equipamento/{equipamento.id}')


#SETORES VINCULADOS AO EQUIPAMENTO
def vincula_setor(request, id):
    #verifica se usuario esta autenticado
    if not request.user.is_authenticated:
        return redirect('/auth/login')
    
    try:
        equipamento = Equipamento.objects.get(pk=id)
        
        setores_temp = equipamento.equipamentosetor_set.all()
        equip_setores = [row.setor.descricao for row in setores_temp]

        setores = Setor.objects.exclude(descricao__in=equip_setores).order_by('descricao')

        if len(setores) == 0:
            messages.add_message(request, constants.ERROR, 'Equipamento já está vinculado a todos os setores.')
            return redirect('/equipamento/')
        context = {
            'equipamento': equipamento,
            'equip_setores': equip_setores,
            'setores': setores
        }
    except:
        messages.add_message(request, constants.ERROR, 'Equipamento não encontrado.')
        return redirect('/equipamento/')

    if request.method == 'GET':
        return render(request, 'vincula_setor.html', context)
    elif request.method == 'POST':
        setor = request.POST.get('setor')
        validade = int(request.POST.get('validade'))
        
        try:
            setor = Setor.objects.get(pk=setor)
        except:
            messages.add_message(request, constants.ERROR, 'Setor inválido.')
            return redirect('/equipamento/')

        if not validade > 0:
            messages.add_message(request, constants.ERROR, 'Validade inválida.')
            return redirect('/equipamento/')

        try:
            EquipamentoSetor.objects.create(equipamento=equipamento, setor=setor, validade=validade)
            messages.add_message(request, constants.SUCCESS, 'Setor vinculado com sucesso.')
            return redirect(f'/equipamento/edicao/{id}')
        except:
            messages.add_message(request, constants.ERROR, 'Não foi possível vincular o Setor ao Equipamento.')
            return redirect('/equipamento/')


def edicao_equipsetor(request, id, id_setor):
    ...


def exclusao_equipsetor(request, id_equip, id_setor):
    #verifica se usuario esta autenticado
    if not request.user.is_authenticated:
        return redirect('/auth/login')        

    try:
        equipamento = Equipamento.objects.get(pk=id_equip)
        setor = Setor.objects.get(pk=id_setor)
        equipsetor = EquipamentoSetor.objects.get(equipamento=equipamento, setor=setor)

        context = {
            'equipamento': equipamento,
            'setor': setor,
            'equipsetor': equipsetor
        }
    except:
        messages.add_message(request, constants.ERROR, 'Equipamento ou Setor inválido.')
        return redirect('/equipamento/')
    
    setores_vinculados = [row.setor.descricao for row in equipamento.equipamentosetor_set.all()]
    if len(setores_vinculados) == 1:
        messages.add_message(request, constants.ERROR, 'O Equipamento deve ter pelo menos um Setor vinculado.')
        return redirect('/equipamento/')

    if request.method == 'GET':
        return render(request, 'exclusao_equipsetor.html', context)
    elif request.method == 'POST':
        try:
            equipsetor.delete()
            messages.add_message(request, constants.SUCCESS, 'Setor removido do Equipamento com sucesso.')
            return redirect('/equipamento/')
        except:
            messages.add_message(request, constants.ERROR, 'Erro ao remover o Setor do Equipamento.')
            return redirect('/equipamento/')
    
