from django.urls import path
from . import views

urlpatterns = [
    path('', views.equipamentos, name='equipamentos'),
    path('cadastro', views.cadastro, name='cadastro_equipamento'),
    path('edicao/<int:id>', views.edicao, name='edicao_equipamento'),
    path('edicao_equipsetor/<int:id>/<int:id_setor>', views.edicao_equipsetor, name='edicao_equipsetor'),
    path('edicao/<int:id>', views.edicao, name='edicao_equipamento'),
    path('exclusao/<int:id>', views.exclusao, name='exclusao_equipamento'),
    path('exclusao/<int:id_equip>/<int:id_setor>', views.exclusao_equipsetor, name='exclusao_equipsetor'),
    path('vincula_setor/<int:id>', views.vincula_setor, name='vincula_setor'),
]