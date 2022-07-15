from django.urls import path
from . import views

urlpatterns = [
    path('', views.setores, name='setores'),
    path('cadastro', views.cadastro, name='cadastro_setor'),
    path('edicao/<int:id>', views.edicao, name='edicao_setor'),
    path('exclusao/<int:id>', views.exclusao, name='exclusao_setor'),
]