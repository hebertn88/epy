from django.urls import path
from . import views

urlpatterns = [
    path('', views.funcionarios, name='funcionarios'),
    path('cadastro', views.cadastro, name='cadastro_funcionario'),
    path('edicao/<int:id>', views.edicao, name='edicao_funcionario'),
    path('exclusao/<int:id>', views.exclusao, name='exclusao_funcionario'),
]